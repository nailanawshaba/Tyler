from xbee import XBee
from serial import Serial
from struct import *

PEGGY_ADDRESS = '\xE0\x03'
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600

cmd_SwitchDisplayMode = 0
cmd_SetDate = 1
cmd_SetTime = 2
cmd_SetWeather = 3

displayMode_Sleep = 0
displayMode_Weather = 1
displayMode_Sonos = 2

weather_conditions = {
    'Sunny' : 0,
    'Rainy' : 1,
    'Cloudy' : 2,
    'Foggy' : 3,
    'Snowy' : 4
}

def set_display_mode(displayMode):
    data = pack('BB', cmd_SwitchDisplayMode, displayMode)
    return send_command(data);

def send_time(hours, minutes):
    data = pack('BBBBB', cmd_SetTime, hours / 10, hours % 10, minutes / 10, minutes % 10)
    return send_command(data)

def send_date(year, month, day):
    data = pack('BBBBBBB', cmd_SetDate, day / 10, day % 10, month / 10, month % 10, year / 10, year % 10)
    return send_command(data)
    
def send_weather(temperature, humidity, condition):
    data = pack('BBBB', cmd_SetWeather, temperature, humidity, int(weather_conditions[condition]))
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
