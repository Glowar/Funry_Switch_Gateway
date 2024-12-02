import asyncio
import config
import function

      
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
    while True:
        if config.qMqtt2Switch:
            try:
                k = config.qMqtt2Switch.popleft()
                writer.write(function.commands(k.slave, k.key, k.state))
                await writer.drain()
            except:
                print(f"TCP: Client suddenly closed, cannot send")
                break
        await asyncio.sleep(0.05)    
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

