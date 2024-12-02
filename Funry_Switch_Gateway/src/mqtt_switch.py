import asyncio
import paho.mqtt.client as mqtt
import config
import json

global mqttcon
global mqtt_keys 
mqtt_keys = bytearray(1536)


def on_disconnect(client, userdata, flags, reason_code, properties):
    global mqttcon
    global mqtt_keys 
    mqttcon = 0
    
    print(f"MQTT: Disconnect")
    

    # The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    global mqttcon
    global mqtt_keys 
    mqttcon = 1
    mqtt_keys.clear()
    mqtt_keys = bytearray(1536)
    
    print(f"MQTT: Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    config.configPublish = 1
    client.subscribe(config.MQTT_TOPIC + "/Set/#")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" m: "+str(msg.payload))
    
def state(client, userdata, message):
    #print(message.topic+" m: "+str(message.payload))
    try:
        data = json.loads(message.payload)
        config.qMqtt2Switch.append(config.Key(int(data['Slave']), int(data['Key']), int(data['State'])))
        print('MQTT: -->>  Slave: ' + data['Slave'] + ', Key: ' + data['Key'] + ', State: ' + data['State'])
    except ValueError:
            return False
    return True    

def configMsg (slave, key):
    return '{"name":"Key ' + ('{:0>3}'.format(str(key))) + '","command_topic":"'+ config.MQTT_TOPIC + '/Set","payload_on":"{ \\"Slave\\": \\"' + str(slave) + '\\", \\"Key\\": \\"' + str(key) + '\\", \\"State\\": \\"1\\" }","payload_off":"{ \\"Slave\\": \\"' + str(slave) + '\\", \\"Key\\": \\"' + str(key) + '\\", \\"State\\": \\"0\\" }","state_topic":"' + config.MQTT_TOPIC + '/Switch' + str(slave) + '/Key' + str(key) + '","state_on":"1","state_off":"0","optimistic":"true","retain":"false","unique_id":"Funry ' + ('{:0>3}'.format(str(slave))) + '{:0>3}'.format(str(key)) + '","device":{"identifiers":["Funry ' + ('{:0>3}'.format(str(slave))) + '"],"name":"Funry ' + ('{:0>3}'.format(str(slave))) + '", "manufacturer": "Funry", "model": "4"}}'

async def mqtt_funry():
    global mqttcon
    global mqtt_keys 
    mqttcon = 0
    
    while True:
        try:
            print('MQTT: Start ...') 
            mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            mqttc.on_connect = on_connect
            mqttc.on_message = on_message
            mqttc.on_disconnect = on_disconnect
            mqttc.username_pw_set(username=config.MQTT_USERNAME, password=config.MQTT_PASSWORD)

            mqttc.message_callback_add(config.MQTT_TOPIC + "/Set", state)
            mqttc.connect(config.MQTT_BROKER, config.MQTT_PORT, 60)
            mqttc.subscribe(config.MQTT_TOPIC + "/Set/#")
            mqttc.loop_start()
            break
        except:
            print("MQTT: Connection failed")
            await asyncio.sleep(5)

    
    print('MQTT: While ...') 
    
    while True:
        if mqttcon == 1:
            if config.configPublish != 0:
                config.configPublish = 0
                #print('MQTT: PublishConfig ...')
                #for i in range (1, 256):
                #    mqttc.publish('homeassistant/switch/key' + str(i) + '/config', configMsg(1, i))
                #    await asyncio.sleep(0.01) 
                #print('MQTT: PublishConfig finish')            
            if config.qSwitch2Mqtt:
                k = config.qSwitch2Mqtt.popleft()
                if mqtt_keys[(k.slave*6)+k.key] != 1:
                    mqttc.publish('homeassistant/switch/Switch' + str(k.slave) + 'Key' + str(k.key) + '/config', configMsg(k.slave, k.key))
                    mqtt_keys[(k.slave*6)+k.key] = 1
                    print(((k.slave*6)+k.key))
                print(((k.slave*6)+k.key))
                mqttc.publish(config.MQTT_TOPIC + '/Switch' + str(k.slave) +  '/Key' + str(k.key), k.state)
                print(f"MQTT: <<--  Slave: {str(k.slave)} Key: {str(k.key)}, State: {str(k.state)}")                                                                                        
        await asyncio.sleep(0.05)
        
        