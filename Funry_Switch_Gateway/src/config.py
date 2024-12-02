from collections import deque

# Protocol AA55
#   Byte num   |      Range    |   Description        
#       0               AA          Static
#       1               55          Static
#       2               01          Static
#       3               00          Static
#       4               04          Static
#       5               01-FE       Адрес кнопи (00 - Not use; FF - ALL Key)
#       6               00/01       Статус выключателя 00 – Выключить; 01 - Включить
#       7               80          Static
#       8               0F          Static
#       9               CRC         0xFF - Byte 5,6,7,8,9.
#       10              5A          Static

# ALL OFF   #AA#55#01#00#04#FF#00#80#0F#6E#5A
# ALL ON    #AA#55#01#00#04#FF#01#80#0F#6D#5A

command_prefix =    bytes(b'\xAA\x55\x01\x00\x04')
command_postfix =   bytes(b'\x80\x0F')
command_end =       bytes(b'\x5A')

command_1_off = b'\xAA\x55\x01\x00\x04\x01\x00\x80\x0F\x6C\x5A' # 1 OFF
command_2_off = b'\xAA\x55\x01\x00\x04\x02\x00\x80\x0F\x6B\x5A' # 2 OFF
command_3_off = b'\xAA\x55\x01\x00\x04\x03\x00\x80\x0F\x6A\x5A' # 3 OFF
command_4_off = b'\xAA\x55\x01\x00\x04\x04\x00\x80\x0F\x69\x5A' # 4 OFF

command_1_on = b'\xAA\x55\x01\x00\x04\x01\x01\x80\x0F\x6B\x5A' # 1 ON
command_2_on = b'\xAA\x55\x01\x00\x04\x02\x01\x80\x0F\x6A\x5A' # 2 ON
command_3_on = b'\xAA\x55\x01\x00\x04\x03\x01\x80\x0F\x69\x5A' # 3 ON
command_4_on = b'\xAA\x55\x01\x00\x04\x04\x01\x80\x0F\x68\x5A' # 4 ON

#
MODE = "TCP"
PROTOCOL = "Modbus" # "Modbus" or "AA55"

# TCP
TCP_HOST = "0.0.0.0"                 # Symbolic name meaning all available interfaces
TCP_PORT = 10502                     # Arbitrary non-privileged port

# MQTT
MQTT_BROKER  = "192.168.1.116"
MQTT_PORT  = 1883
MQTT_TOPIC  = "Funry"
MQTT_CLIENT_ID  = "funry"
MQTT_USERNAME  = "mqtt"
MQTT_PASSWORD  = "Aa123592"

# Serial
SERIAL_PORT = 'COM8'  # Change this to your actual port
SERIAL_RATE = 57600   # Change this to your desired baud rate

# Global
class Key:
    def __init__(self, slave, key, state):
        self.slave = slave
        self.key = key
        self.state = state
        
qMqtt2Switch = deque()
qSwitch2Mqtt = deque()

configPublish = 0
