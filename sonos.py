import sys
from time import sleep
from soco import SoCo
from soco import SonosDiscovery

# TODO
#    - What if multiple devices try to connect at the same time?
#    - Better overall error handling
#    - the schema strings are ugly, use () over multiple lines to make them look better

class SonosController:

    _device = None

    def connect(self):
	ips = []
	while (len(ips) == 0):
	    print "No Sonos found"
	    sonos_devices = SonosDiscovery()
	    ips = sonos_devices.get_speaker_ips()
	
        print "Found {0} device(s)".format(len(ips))

	for ip in ips:
	    self._device = SoCo(ip)
	    zone_name = self._device.get_speaker_info()['zone_name']
	    print "IP of {0} is {1}".format(zone_name, ip)

    def get_current_song(self):
	if self._device == None:
	    self.connect()

	now_playing = self._device.get_current_track_info()
	return now_playing

    def play_pandora_station(self, code):
	if self._device == None:
	    self.connect()
	
	PLAY_STATION_ACTION ='"urn:schemas-upnp-org:service:AVTransport:1#SetAVTransportURI"'
	TRANSPORT_ENDPOINT = '/MediaRenderer/AVTransport/Control'
	JOIN_RESPONSE = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetAVTransportURIResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:SetAVTransportURIResponse></s:Body></s:Envelope>'
	PLAY_STATION_BODY_TEMPLATE ='"<u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><CurrentURI>pndrradio:{music_service_station_id}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData></u:SetAVTransportURI></s:Body></s:Envelope>'
	
	body = PLAY_STATION_BODY_TEMPLATE.format(music_service_station_id = code)
	response = self._device.send_command(TRANSPORT_ENDPOINT, PLAY_STATION_ACTION, body)
	
	if (response == JOIN_RESPONSE):
	    self._device.play()
	    return True
	else:
	    return self._device.parse_error(response)

    def pause(self):
	if self._device == None:
	    connect()

	try:
	    self._device.pause()
	except:
            print "Error trying to pause music: there is probably nothing playing right now."
	    return False
	
	return True
