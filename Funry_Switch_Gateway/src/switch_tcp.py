import asyncio
import config
import function
import time
from mqtt_switch import mqtt_keys
       

async def handle_read(reader, writer, addr):
    while True:
        # Receive
        try:
            data = await reader.read(64)
            if not data:
                break
            function.rxDataProccesing(data)
        except:
            print(f"TCP: Client suddenly closed while receiving from {addr}")
            break
    writer.close()
    await writer.wait_closed()
    print("TCP: Disconnected R by", addr)  

async def handle_write(writer, addr):
    global mqtt_keys 
    i = 1
    n = 1
    lasttime = 0
    
    while True:

        if config.qMqtt2Switch:
            try:
                laptime  = 0
                k = config.qMqtt2Switch.popleft()
                writer.write(function.commands(k.slave, k.key, k.state))
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
                    writer.write(function.commands(i, n, 1))
                    await writer.drain()
                    n += 1
                    if n > 6:
                        n = 1
                        i += 1
                        if i > 254:
                            i = 1
                except:
                    print(f"TCP: Client suddenly closed, cannot send")
                    break
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

