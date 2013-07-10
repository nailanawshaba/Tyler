from sources import XBeeListener
from sinks import XivelySink

class Sonometer:
    """Sonometer sensor"""
    
    name = "Sonometer"

    def __init__(self, listener, sink):
        self.__listener = listener
        self.__listener.register("SONO", self.newValueReady)
        self.__sink = sink

    def newValueReady(self, value):
        # Do something with the value, or not, then send it to the sink
        mean = sum(value) / len(value)
        self.__sink.update(self.name, mean)
