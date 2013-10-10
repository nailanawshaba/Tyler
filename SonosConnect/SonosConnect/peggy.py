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

def send_time(h1, h2, m1, m2):
    ser = Serial(SERIAL_PORT, BAUD_RATE)
    xbee = XBee(ser)

    data = pack('BBBBB', cmd_SetTime, h1, h2, m1, m2)

    try:
        xbee.tx(dest_addr=PEGGY_ADDRESS, data=data)
        ser.close()
        return True
    except:
        ser.close()
        return False


def send_command(command, parameter):
    ser = Serial(SERIAL_PORT, BAUD_RATE)
    xbee = XBee(ser)

    data = pack('BB', command, parameter)

    try:
        xbee.tx(dest_addr=PEGGY_ADDRESS, data=data)
        ser.close()
        return True
    except:
        ser.close()
        return False
    
def send_text(text):
    ser = Serial(SERIAL_PORT, BAUD_RATE)
    xbee = XBee(ser)
    try:
        xbee.tx(dest_addr=PEGGY_ADDRESS, data=text.upper())
        ser.close()
        return True
    except:
        ser.close()
        return False
