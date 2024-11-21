import asyncio
from switch_tcp import funry_tcp
from serial_switch import serial_funry
from mqtt_switch import mqtt_funry
import nest_asyncio
import config

nest_asyncio.apply()

async def main():
    print('Start ...')    

    if config.MODE:
        task_tcp = asyncio.create_task(funry_tcp())
    else:
        task_serial = asyncio.create_task(serial_funry())
    task_mqtt = asyncio.create_task(mqtt_funry())

    if config.MODE:
        await task_tcp
    else:        
        await task_serial
        
    await task_mqtt
    
asyncio.run(main())
print('FINISH')
