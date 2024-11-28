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
        server_type = conf.get("server_type", "TCP")
        
    if server_type != "tcp" and server_type != "serial":
        print("Unsupported server type")
        exit(1)    
        
    if config.MODE !=0:
        task_tcp = asyncio.create_task(funry_tcp())
    else:
        task_serial = asyncio.create_task(serial_funry())
    task_mqtt = asyncio.create_task(mqtt_funry())

    if config.MODE !=0:
        await task_tcp
    else:        
        await task_serial
        
    await task_mqtt
    
asyncio.run(main())
print('FINISH')
