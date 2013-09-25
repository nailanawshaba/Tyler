import sys
from time import sleep
from soco import SoCo
from soco import SonosDiscovery

from xbee import XBee
from serial import Serial

PEGGY_ADDRESS = '\xE0\x03'

def find_sonos():
    ips = []
    while (len(ips) == 0):
        print "No Sonos found"
        sonos_devices = SonosDiscovery()
        ips = sonos_devices.get_speaker_ips()

    return ips

def send_to_peggy(text):
    ser = Serial("/dev/ttyAMA0", 9600)
    xbee = XBee(ser)
    try:
        xbee.tx(dest_addr=PEGGY_ADDRESS, data=text.upper())
        ser.close()
        return True
    except:
        ser.close()
        return False


def is_same_song(song1, song2):
    if song1 == None or song2 == None:
        return False
    
    if song1['artist'] == song2['artist'] and song1['title'] == song2['title'] and song1['album'] == song2['album']:
        return True

    return False


def run():
    ips = find_sonos()
    print "Found {0} device(s)".format(len(ips))
    for ip in ips:
        device = SoCo(ip)
        zone_name = device.get_speaker_info()['zone_name']
        print "IP of {0} is {1}".format(zone_name, ip)
           
        now_playing = None

        while True:
            try:
                tmp = device.get_current_track_info()
                if not is_same_song(now_playing, tmp):     
                    now_playing = tmp
                    print "Now Playing: {0} - {1} ({2})".format(now_playing['artist'], now_playing['title'], now_playing['album'])
                    send_to_peggy("{0}:{1}".format(now_playing['artist'], now_playing['title']))
                sleep(20)
            except KeyboardInterrupt:
                break
    
run()
