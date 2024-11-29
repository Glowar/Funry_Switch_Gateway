import asyncio
from switch_tcp import funry_tcp
from serial_switch import serial_funry
from mqtt_switch import mqtt_funry
import nest_asyncio
import config
import json
import os

nest_asyncio.apply()

async def main():
    print('Start ...')    
    try:
        with open("/data/options.json") as f:
            conf = json.load(f)
         
            config.MODE = conf.get("mode", "TCP")
            config.PROTOCOL = conf.get("protocol", "Modbus")
            config.TCP_HOST = conf.get("listen_address", "0.0.0.0")
            config.TCP_PORT = conf.get("listen_port", 10502)
            config.MQTT_BROKER = conf.get("mqtt_address", "192.168.1.121")
            config.MQTT_PORT = conf.get("mqtt_port", 1883)
            config.MQTT_TOPIC = conf.get("mqtt_topic", "Funry/Switch/State")
            config.MQTT_USERNAME = conf.get("mqtt_user", "mqtt")
            config.MQTT_PASSWORD = conf.get("mqtt_password", "Aa123592")
            config.SERIAL_PORT = conf.get("serial_port", "COM8")
            config.SERIAL_RATE = conf.get("serial_rate", 9600)

    except:
         print('Couldnt open the settings file')               
        
    if config.MODE != "TCP" and config.MODE != "SERIAL" and config.MODE != 2:
        print("Unsupported server type")
        exit(1)    
        
    if config.MODE == "SERIAL":
        task_serial = asyncio.create_task(serial_funry())
    else:
        task_tcp = asyncio.create_task(funry_tcp())
        
    task_mqtt = asyncio.create_task(mqtt_funry())

    if config.MODE == "SERIAL":
        await task_serial
    else:        
        await task_tcp
        
    await task_mqtt
    
asyncio.run(main())
print('FINISH')
