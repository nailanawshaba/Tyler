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
            
