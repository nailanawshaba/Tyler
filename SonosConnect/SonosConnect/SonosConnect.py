import sys
from time import sleep
from soco import SoCo
from soco import SonosDiscovery

device = None
now_playing = None

def find_sonos():
    ips = []
    while (len(ips) == 0):
        print "No Sonos found"
        sonos_devices = SonosDiscovery()
        ips = sonos_devices.get_speaker_ips()

    return ips

def connect():
    ips = find_sonos()
    print "Found {0} device(s)".format(len(ips))

    for ip in ips:
        global device
        device = SoCo(ip)
        zone_name = device.get_speaker_info()['zone_name']
        print "IP of {0} is {1}".format(zone_name, ip)

def get_current_song():
    global device
    if device != None:
        connect()

    now_playing = device.get_current_track_info()
    return now_playing

def play_pandora_station(code):
    global device
    PLAY_STATION_ACTION ='"urn:schemas-upnp-org:service:AVTransport:1#SetAVTransportURI"'
    TRANSPORT_ENDPOINT = '/MediaRenderer/AVTransport/Control'
    JOIN_RESPONSE = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetAVTransportURIResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:SetAVTransportURIResponse></s:Body></s:Envelope>'
    PLAY_STATION_BODY_TEMPLATE ='"<u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><CurrentURI>pndrradio:{music_service_station_id}</CurrentURI><CurrentURIMetaData></CurrentURIMetaData></u:SetAVTransportURI></s:Body></s:Envelope>'
    
    body = PLAY_STATION_BODY_TEMPLATE.format(music_service_station_id = code)
    response = device.send_command(TRANSPORT_ENDPOINT, PLAY_STATION_ACTION, body)
    
    if (response == JOIN_RESPONSE):
        device.play()
        return True
    else:
        return device.parse_error(response)

