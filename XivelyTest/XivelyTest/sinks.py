import datetime
import xively

DEBUG = False

class XivelySink:
    """connects to  Xively and uploads data"""

    __apiKey = "<API KEY>"

    def __init__(self, feed_id):
        self.__api = xively.XivelyAPIClient(self.__apiKey)
        self.__feed = self.__api.feeds.get(feed_id)

    def update(self, source, value):
        datastream = self.__get_datastream(source)
        datastream.current_value = value
        datastream.at = datetime.datetime.utcnow()
        try:
            datastream.update()
        except requests.HTTPError as e:
            print("HTTPError({0}): {1}".format(e.errno, e.strerror))

    def __get_datastream(self, datastream_name):
        try:
            datastream = self.__feed.datastreams.get(datastream_name)
            if DEBUG:
                print("Found existing datastream")
            return datastream
        except:
            if DEBUG:
                print("Creating new datastream")
            datastream = self.__feed.datastreams.create(datastream_name, tags="test")
        return datastream