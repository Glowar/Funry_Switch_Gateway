import config

def rxDataProccesing(data):
    index = data.find(b'\x5A')
    if  index > 9:
            #print('5A')
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
            config.qSwitch2Mqtt.append(config.Key(Key, State))
            print('Switch: -->>  Key: ' + str(Key) + ', State: ' + str(State))
            
def getcrc (commands):
    
    crc = 255
    for i in range(4, 9):
        crc = crc - commands[i]   
        if crc < 0:
            crc += 255
            crc += 1      
            
    crc += 1        
    return crc.to_bytes()

def commands (key, state):
   
    commands_array = bytearray()
    commands_array.extend(config.command_prefix)
    commands_array.append(key)
    commands_array.append(state)
    commands_array.extend(config.command_postfix)
    commands_array.extend(getcrc(commands_array))
    commands_array.extend(config.command_end)
    print('Switch: <<--  Key: ' + str(key) + ', State: ' + str(state))
    return commands_array            
