import asyncio
import config
import function
import time
from mqtt_switch import mqtt_keys
global rxNewData
global RxBuf
global wait_response
global Response
RxBuf = bytearray()
rxNewData = False    
wait_response = False   

async def wait_response_fun():
    global rxNewData
    
    while rxNewData != True:
        await asyncio.sleep(0.01)
    return 1

async def handle_read(reader, writer, addr):
    global Response
    global rxNewData
    global RxBuf
    global wait_response
   
    while True:
        # Receive
        try:
            data = await reader.read(64)
            if not data:
                break
            #print("Data: ", data)
            Fun = int(data[7])
            if Fun == 6:
                function.rxDataProccesing(data)
            else:                
                Response = function.rxResponseProccesing(data)
                rxNewData = True
        except:
            print(f"TCP: Client suddenly closed while receiving from {addr}")
            break
    writer.close()
    await writer.wait_closed()
    print("TCP: Disconnected R by", addr)  

async def handle_write(writer, addr):
    global rxNewData
    global RxBuf
    global wait_response
    global mqtt_keys 
    i = 1
    n = 1
    lasttime = 0
    
    while True:

        if config.qMqtt2Switch:
            try:
                laptime  = 0
                k = config.qMqtt2Switch.popleft()
                writer.write(function.commandKeyStateSet(k.slave, k.key, k.state))
                await writer.drain()
            except:
                print(f"TCP: Client suddenly closed, cannot send")
                break
        else:
            laptime = round((time.time() - lasttime), 2)
            if laptime  > 1:
                laptime  = 0
                lasttime = time.time()
                try:
                    #mqtt_keys[(i*6)+n] = 0
                    rxNewData = False
                    writer.write(function.commandKeyStateGet(i, n))
                    try:
                        await asyncio.wait_for(writer.drain(),timeout=0.1)
                        await asyncio.wait_for(wait_response_fun(), timeout=0.1)
                        if Response[0] == i:
                            config.qSwitch2Mqtt.append(config.Key(Response[0], n, Response[1]))
                            print('Switch: (Slave: ' + str(Response[0]) + ', Key: ' + str(n) + ', State: ' + str(Response[1]) + ') -->>')
                    except:
                        print(f"TCP: No response")
                    n += 1
                    if n > 6:
                        n = 1
                        i += 1
                        if i > 254:
                            i = 1
                except:
                    #continue
                    print(f"TCP: Client suddenly closed, cannot send")
        wait_response = False
        await asyncio.sleep(0.1)          
    writer.close()
    await writer.wait_closed()
    print("TCP: Disconnected W by", addr)    
        
async def handle_client(reader, writer):

    config.qMqtt2Switch.clear()
    addr = writer.get_extra_info("peername")
    print(f"TCP: New connection: {addr}")

    asyncio.create_task(handle_read(reader, writer ,addr))
    asyncio.create_task(handle_write(writer, addr))
    
    
async def funry_tcp():
    print('TCP: Start ...')
        
    server = await asyncio.start_server(
        handle_client, config.TCP_HOST, config.TCP_PORT)
    addr = server.sockets[0].getsockname()
    print(f'TCP: Serving on {addr}')
    async with server:
        await server.serve_forever()
        
    print('TCP: End')

