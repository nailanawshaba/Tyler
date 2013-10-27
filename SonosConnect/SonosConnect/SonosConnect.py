import sys
from time import sleep
from soco import SoCo
from soco import SonosDiscovery

from xbee import XBee
from serial import Serial

from peggy import send_music_data

PEGGY_ADDRESS = '\xE0\x03'

device = None
now_playing = None

def find_sonos():
    ips = []
    while (len(ips) == 0):
        print "No Sonos found"
        sonos_devices = SonosDiscovery()
        ips = sonos_devices.get_speaker_ips()

    return ips

def is_same_song(song1, song2):
    if song1 == None or song2 == None:
        return False
    
    if song1['artist'] == song2['artist'] and song1['title'] == song2['title'] and song1['album'] == song2['album']:
        return True

    return False

def connect():
    ips = find_sonos()
    print "Found {0} device(s)".format(len(ips))

    for ip in ips:
        global device
        device = SoCo(ip)
        zone_name = device.get_speaker_info()['zone_name']
        print "IP of {0} is {1}".format(zone_name, ip)

def update_song_info():
    global device
    global now_playing

    if device != None:
        tmp = device.get_current_track_info()
        if not is_same_song(now_playing, tmp):     
            now_playing = tmp
            send_music_data(now_playing['artist'], now_playing['album'], now_playing['title'])
       
def play_pandora_station(email, title, code):
    PLAY_STATION_ACTION ='"urn:schemas-upnp-org:service:AVTransport:1#SetAVTransportURI"'
    PLAY_STATION_BODY_TEMPLATE ='"<u:SetAVTransportURI xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><CurrentURI>{music_service}:{music_service_station_id}</CurrentURI><CurrentURIMetaData>&lt;DIDL-Lite xmlns:dc=&quot;http://purl.org/dc/elements/1.1/&quot; xmlns:upnp=&quot;urn:schemas-upnp-org:metadata-1-0/upnp/&quot;xmlns:r=&quot;urn:schemas-rinconnetworks-com:metadata-1-0/&quot; xmlns=&quot;urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/&quot;&gt;&lt;item id=&quot;OOOX{music_service_station_id}&quot; parentID=&quot;0&quot; restricted=&quot;true&quot;&gt;&lt;dc:title&gt;{music_service_station_title}&lt;/dc:title&gt;&lt;upnp:class&gt;object.item.audioItem.audioBroadcast&lt;/upnp:class&gt;&lt;desc id=&quot;cdudn&quot; nameSpace=&quot;urn:schemas-rinconnetworks-com:metadata-1-0/&quot;&gt;SA_RINCON3_{music_service_email}&lt;/desc&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;</CurrentURIMetaData></u:SetAVTransportURI></s:Body></s:Envelope>'
    PANDORA_SERVICE = 'pndrradio'
    #TRANSPORT_ENDPOINT = '/MediaRenderer/AVTransport/Control'
    #JOIN_RESPONSE = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetAVTransportURIResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:SetAVTransportURIResponse></s:Body></s:Envelope>'

    body = PLAY_STATION_BODY_TEMPLATE.format(music_service = PANDORA_SERVICE, music_service_station_title = title, music_service_station_id = code, music_service_email = email)
    response = self.__send_command(TRANSPORT_ENDPOINT, PLAY_STATION_ACTION, body)

    if (response == JOIN_RESPONSE):
        return True
    else:
        return self.__parse_error(response)

