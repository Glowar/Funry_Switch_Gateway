import config
import math

def rxDataProccesing(data):
    #print('Data: ', data)
    if config.PROTOCOL == "Modbus":
        if data[3:5] == bytes(b'\x00\x00'):
            #print('Data pref: ', data[2:5])
            Len = int(data[5])
            if Len > 5 and Len < 7:
                #print('Data len: ', Len)
                Slave = int(data[6])
                if Slave > 0 and Slave < 255:
                    #print('Data Slave: ', Slave)
                    Fun = int(data[7])
                    if Fun == 6:
                        #print('Data Fun: ', Fun)
                        if int(data[8]) == 16:
                            Key = int(data[9]) - 32
                            if Key > 0 and Key < 7:
                                #print('Data Key: ', Key)
                                #if int(data[10]) == 0:
                                State = int(data[11])
                                #print('Data State: ', State)
                                #config.qSwitch2Mqtt.append(config.Key((((Slave - 1) * 4) + Key), State))
                                config.qSwitch2Mqtt.append(config.Key(Slave, Key, State))
                                print('Switch: (Slave: ' + str(Slave) + ', Key: ' + str(Key) + ', State: ' + str(State) + ') -->>')
    else:
        index = data.find(b'\x5A')
        if  index > 9:
                #del com[index:]
                #print(com)
                #del data[2:8]
                #print(data)
                #print(ord(data[(index-9)]))
                #print([data[index-10:index+1]])
                #print(data[index-10:index-5])
                #print(config.command_prefix)
            if data[index-10:index-5] == config.command_prefix:
                #print('Prefix')
                Key = data[index-5]
                State = data[index-4]
                config.qSwitch2Mqtt.append(config.Key(0, Key, State))
                print('Switch: (Key: ' + str(Key) + ', State: ' + str(State) + ') -->>')
            
def getcrc (commands):
    
    crc = 255
    for i in range(4, 9):
        crc = crc - commands[i]   
        if crc < 0:
            crc += 255
            crc += 1      
            
    crc += 1        
    return crc.to_bytes()

def commands (Slave, Key, State):
   
    commands_array = bytearray()
    if config.PROTOCOL == "Modbus":
        #Slave = math.ceil(Key / 4) 
        #Key = Key - ((Slave*4)-4)
        commands_array.extend(b'\x00\x00\x00\x00\x00\x06')
        commands_array.append(Slave)
        commands_array.extend(b'\x06\x10')
        commands_array.append(Key+32)
        commands_array.append(0)
        commands_array.append(State)
        #\x21\x00\x01')
        print('Switch: (Slave: ' + str(Slave) + ', Key: ' + str(Key) + ', State: ' + str(State) + ') <<--')
    else:        
        commands_array.extend(config.command_prefix)
        commands_array.append(Key)
        commands_array.append(State)
        commands_array.extend(config.command_postfix)
        commands_array.extend(getcrc(commands_array))
        commands_array.extend(config.command_end)
        print('Switch: (Key: ' + str(Key) + ', State: ' + str(State) + ') <<--')
    return commands_array            