import asyncio
import serial_asyncio
import config
import function
    
    
class OutputProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        config.qMqtt2Switch.clear()
        self.transport = transport
        print('port opened', transport)
        transport.serial.rts = False  # You can manipulate Serial object via transport
        
    def data_received(self, data):
        function.rxDataProccesing(data)
        self.resume_reading()                          

    def connection_lost(self, exc):
        print('SERIAL: port closed')
        self.transport.loop.stop()

    def pause_writing(self):
        print('SERIAL: pause writing')
        print(self.transport.get_write_buffer_size())

    def resume_writing(self):
        print(self.transport.get_write_buffer_size())
        print('SERIAL: resume writing')
        
    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        self.transport.resume_reading()   
        
             
async def serial_funry():
    print('SERIAL: Start ...') 
    loop = asyncio.get_event_loop()
    coro = serial_asyncio.create_serial_connection(loop, OutputProtocol, config.SERIAL_PORT, baudrate=config.SERIAL_RATE)
    transport, protocol = loop.run_until_complete(coro)
    
    #for i in range (1, 255):
    #    transport.write(commands(i,0))
    #    await asyncio.sleep(0.04)

    #for i in range (1, 255):
    #    transport.write(commands(i,1))
    #    await asyncio.sleep(0.04)
      
    #transport.write(commands(1,config.ON))
    #await asyncio.sleep(0.1)               
    #transport.write(commands(2,config.ON))
    #await asyncio.sleep(0.1)
    #transport.write(commands(3,config.ON))
    #await asyncio.sleep(0.1)
    #transport.write(commands(4,config.ON))
    #await asyncio.sleep(0.1)
    #transport.write(commands(1,config.OFF))
    #await asyncio.sleep(0.1)
    #transport.write(commands(2,config.OFF))
    #await asyncio.sleep(0.1)
    #transport.write(commands(3,config.OFF))
    #await asyncio.sleep(0.1)
    #transport.write(commands(4,config.OFF))
    #await asyncio.sleep(0.2)
    #transport.write(commands(config.ALL,config.ON))
    #await asyncio.sleep(0.2)
    #transport.write(commands(config.ALL,config.OFF))
    #await asyncio.sleep(0.2)
     
    #loop.run_forever()
    print('SERIAL: While ...') 
    while True:
        if config.qMqtt2Switch:
            #print(config.q.popleft())
            k = config.qMqtt2Switch.popleft()
            transport.write(function.commandKeyStateSet(k.slave, k.key, k.state))
            #print('Serial Write: Key: '+ str(k.key) + ' State: ' + str(k.state))
            #print(k.key)
            #print(k.state)
                                                                                                
        await asyncio.sleep(0.05)

