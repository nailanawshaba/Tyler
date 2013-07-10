import serial
import threading
import datetime
from xbee import XBee

class XBeeListener (threading.Thread):
    """Owns the XBee radio interface. Receives frame from sensors and send commands to sinks."""
    
    __terminate = False
    __handlers = dict()

    def __init__(self, com_port):
        self.__portName = com_port
        threading.Thread.__init__(self)
        
    def run(self):
        serialPort = serial.Serial(self.__portName, 9600)
        xbee = XBee(serialPort)

        while(self.__terminate != True):
            try:
                response = xbee.wait_read_frame()
                self.__parse(response)
            except Exception:
                print('Error waiting for frame at ' + str(datetime.datetime.now()))
        
        serialPort.close();

    def register(self, prefix, function):
        self.__handlers[prefix] = function

    def terminate(self):
        self.__terminate = True

    def __parse(self, xbee_frame):
        frame_length = len(xbee_frame['rf_data'])
        sensor = xbee_frame['rf_data'][0:4].decode("utf-8")
        value = xbee_frame['rf_data'][4:frame_length - 1]
        self.__handlers[sensor](value)