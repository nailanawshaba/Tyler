from xbee import XBee
from serial import Serial
from struct import *

PEGGY_ADDRESS = '\xE0\x03'
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600

cmd_WakeUp = 1
cmd_Sleep = 2
cmd_SwitchDisplayMode = 3

displayMode_Weather = 1
displayMode_Sonos = 2

PEGGYMODE_NOWPLAYING = B'1'

def send_command(command, parameter):
    ser = Serial(SERIAL_PORT, BAUD_RATE)
    xbee = XBee(ser)

    data = pack('B', command, parameter)

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
