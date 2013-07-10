import sys
from time import sleep
from soco import SoCo
from soco import SonosDiscovery


def find_sonos():
    ips = []
    while (len(ips) == 0):
        print "No Sonos found"
        sonos_devices = SonosDiscovery()
        ips = sonos_devices.get_speaker_ips()

    return ips


def run():
    ips = find_sonos()
    print "Found {0} device(s)".format(len(ips))
    for ip in ips:
        device = SoCo(ip)
        zone_name = device.get_speaker_info()['zone_name']
        print "IP of {0} is {1}".format(zone_name, ip)
           
        while True:
            try:     
                now_playing = device.get_current_track_info()
                print "Now Playing: {0} - {1} ({2})".format(now_playing['artist'], now_playing['title'], now_playing['album'])
                sleep(3)
            except:
                continue
    
run()