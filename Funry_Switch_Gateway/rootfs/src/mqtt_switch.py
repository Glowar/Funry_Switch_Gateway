import asyncio
import paho.mqtt.client as mqtt
import config
import json

global mqttcon

def on_disconnect(client, userdata, flags, reason_code, properties):
    global mqttcon
    mqttcon = 0
    print(f"MQTT: Disconnect")
    

    # The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, reason_code, properties):
    global mqttcon
    mqttcon = 1
    print(f"MQTT: Connected with result code {reason_code}")
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    config.configPublish = 1
    client.subscribe(config.TOPIC + "/Set/#")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" m: "+str(msg.payload))
    
def state(client, userdata, message):
    #print(message.topic+" m: "+str(message.payload))
    try:
        data = json.loads(message.payload)
        config.qMqtt2Switch.append(config.Key(int(data['Key']), int(data['State'])))
        print('MQTT: -->>  Key: ' + data['Key'] + ', State: ' + data['State'])
    except ValueError:
            return False
    return True    

def configMsg (key):
    return '{"name":"Key ' + ('ALL' if key == 255 else '{:0>3}'.format(str(key))) + '","command_topic":"'+ config.TOPIC + '/Set","payload_on":"{ \\"Key\\": \\"' + str(key) + '\\", \\"State\\": \\"1\\" }","payload_off":"{ \\"Key\\": \\"' + str(key) + '\\", \\"State\\": \\"0\\" }","state_topic":"' + config.TOPIC + '/Key' + str(key) + '","state_on":"1","state_off":"0","optimistic":"true","retain":"false","unique_id":"Key' + str(key) + '","device":{"identifiers":["Funry"],"name":"Funry"}}'
   
async def mqtt_funry():
    global mqttcon
    mqttcon = 0
    
    while True:
        try:
            print('MQTT: Start ...') 
            mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            mqttc.on_connect = on_connect
            mqttc.on_message = on_message
            mqttc.on_disconnect = on_disconnect
            mqttc.username_pw_set(username=config.USERNAME, password=config.PASSWORD)

            mqttc.message_callback_add(config.TOPIC + "/Set", state)
            mqttc.connect(config.BROKER, config.PORT, 60)
            mqttc.subscribe(config.TOPIC + "/Set/#")
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
                print('MQTT: PublishConfig ...')
                for i in range (1, 256):
                    mqttc.publish('homeassistant/switch/key' + str(i) + '/config', configMsg(i))
                    await asyncio.sleep(0.01) 
                print('MQTT: PublishConfig finish')            
            if config.qSwitch2Mqtt:
                k = config.qSwitch2Mqtt.popleft()
                mqttc.publish(config.TOPIC + '/Key' + str(k.key), k.state)
                print(f"MQTT: <<--  Key: {str(k.key)}, State: {str(k.state)}")                                                                                        
        await asyncio.sleep(0.05)
        
        