from xbee import XBee
from serial import Serial
from struct import *

PEGGY_ADDRESS = '\xE0\x03'
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600

cmd_WakeUp = 0
cmd_Sleep = 1
cmd_SwitchDisplayMode = 2
cmd_SetDate = 3
cmd_SetTime = 4
cmd_SetWeather = 5

displayMode_Weather = 0
displayMode_Sonos = 1


def send_time(hours, minutes):
    data = pack('BBBBB', cmd_SetTime, hours / 10, hours % 10, minutes / 10, minutes % 10)
    return send_command(data)

def send_date(day, month, year):
    data = pack('BBBBBBB', cmd_SetDate, day / 10, day % 10, month / 10, month % 10, year / 10, year % 10)
    return send_command(data)
    
def send_command(data):
    ser = Serial(SERIAL_PORT, BAUD_RATE)
    xbee = XBee(ser)
    try:
        xbee.tx(dest_addr=PEGGY_ADDRESS, data=data)
        ser.close()
        return True
    except:
        ser.close()
        return False
