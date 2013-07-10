from sinks import XivelySink
from sources import XBeeListener
from sensors import Sonometer

SENSORS_FEED = "<FEED ID>"

# main program entry point - runs continuously updating our datastream with the
# current 1 minute load average
def run():
    listener = XBeeListener("COM5")
    sink = XivelySink(SENSORS_FEED)
    sonometer = Sonometer(listener, sink)
    
    print("Starting listener")
    listener.start()
    listener.join()
 
run()
