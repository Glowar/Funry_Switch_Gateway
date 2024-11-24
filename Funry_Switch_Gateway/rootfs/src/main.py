import asyncio
from switch_tcp import funry_tcp
from serial_switch import serial_funry
from mqtt_switch import mqtt_funry
import nest_asyncio
import config
import json

nest_asyncio.apply()

async def main():
    print('Start ...')    
    
    with open("/data/options.json") as f:
        conf = json.load(f)
        addr = conf.get("listen_address", "0.0.0.0")
        port = conf.get("listen_port", "10502")
        server_type = conf.get("server_type", "tcp")
        
    if server_type == "tcp":
        addr = (addr, port)
    elif server_type == "serial":
        addr = addr
    else:
        _logger.critical("Unsupported server type")
        exit(1)        
        
    if server_type == "tcp":
        task_tcp = asyncio.create_task(funry_tcp(addr, port))
    else:
        task_serial = asyncio.create_task(serial_funry(addr))
    task_mqtt = asyncio.create_task(mqtt_funry())

    if config.MODE:
        await task_tcp
    else:        
        await task_serial
        
    await task_mqtt
    
asyncio.run(main())
print('FINISH')
