#!/usr/bin/python

# python standard imports
import json

# external libraries imports
from flask import Flask, request

# project imports
import pandora
import sonos
import weather
import wemo
import peggy

server = Flask(__name__)

peggy_controller = peggy.PeggyController()
sonos_controller = sonos.SonosController()
wemo_controller = wemo.WemoController()

@server.route("/music/nowplaying")
def music_nowplaying():
    nowplaying = sonos_controller.get_current_song()
    urls = nowplaying['album_art'].split('http://')
    album_art = 'http://' + urls[len(urls) - 1]
    response = { 'artist': nowplaying['artist'], 'album': nowplaying['album'], 'title': nowplaying['title'], 'album_art': album_art }
    return json.dumps(response)

@server.route("/music/pandora/stations/<pandora_email>")
def music_pandora_stations(pandora_email):
    user = pandora.get_pandora_user(pandora_email)
    stations = pandora.get_stations(user)
    return json.dumps(stations)

@server.route("/music/pandora/play/<station_code>")
def music_pandora_play(station_code):
    if True == sonos_controller.play_pandora_station(station_code):
        return 'OK'
    else:
        return 'FAIL'

@server.route("/music/pause")
def music_pause():
    print "Pausing..."
    sonos_controller.pause()
    return "OK\r\n"

@server.route("/music/volume", methods = ['GET', 'POST'])
def volume():
    response = None
    print "requesting volume with method " + request.method
    if request.method == 'GET':
        print "getting volume from Sonos"
        vol = sonos_controller.get_volume()
        print "volume is " + str(vol)
        response = str(vol)
    elif request.method == 'POST':
        try:
            desired_vol = json.loads(request.data)['volume']
            sonos_controller.set_volume(int(desired_vol))
            response = json.dumps(str(desired_vol))
        except ValueError:
            response = Response(status = 400)
    
    # Flask takes care of handling return code for bad methods
    return response

@server.route("/peggy/weather")
def peggy_weather():
    global peggy_controller
    peggy_controller.show_weather()
    return "OK\r\n"
    
@server.route("/peggy/nowplaying")
def peggy_music():
    global peggy_controller
    peggy_controller.show_music()
    return "OK\r\n"

@server.route("/peggy/sleep")
def peggy_sleep():
    global peggy_controller
    peggy_controller.sleep();
    return "OK\r\n"

@server.route("/wemo/list")
def wemo_list():
    switches = wemo_controller.find_switches()
    return json.dumps(switches)

@server.route("/wemo/on/<switch_name>")
def wemo_on(switch_name):
    wemo_controller.switch_on(switch_name)
    return "OK"

@server.route("/wemo/off/<switch_name>")
def wemo_off(switch_name):
    wemo_controller.switch_off(switch_name)
    return "OK"

@server.route("/wemo/state/<switch_name>")
def wemo_state(switch_name):
    state = wemo_controller.switch_state(switch_name)
    return json.dumps(state)

if __name__ == "__main__":
    print "Connecting to Sonos"
    sonos_controller.connect()
    print "Connecting to Wemo switches"
    wemo_controller.connect()
    print "Starting Server in debug mode..."
    #server.debug = True
    server.run(host='0.0.0.0')
