from peggy import *
from weather import *
from datetime import *
from time import sleep
from threading import Thread
from flask import Flask
from SonosConnect import connect, get_current_song, play_pandora_station
from pandora import get_pandora_user, get_stations

import json

server = Flask(__name__)

weather_on = False
music_on = False
sleep_on = True

now_playing = None

def is_same_song(song1, song2):
    if song1 == None or song2 == None:
        return False
    
    if song1['artist'] == song2['artist'] and song1['title'] == song2['title'] and song1['album'] == song2['album']:
        return True

    return False

def peggy_weather_loop():
    global sleep_on, music_on, weather_on
    sleep_on = False
    music_on = False
    weather_on = True

    set_display_mode(displayMode_Weather)

    while(weather_on):
        now = datetime.now()
        send_time(now.hour, now.minute)
        send_date(now.year - 2000, now.month, now.day)

        weather = get_current_conditions("98122")
        send_weather(weather['temperature'], weather['humidity'], weather['condition'])

        sleep(10)

def peggy_music_loop():
    global sleep_on, music_on, weather_on
    sleep_on = False
    music_on = True
    weather_on = False

    set_display_mode(displayMode_Sonos)

    global now_playing
    connect()
    while(music_on):
        tmp = get_current_song()
        if not is_same_song(now_playing, tmp):     
            now_playing = tmp
            send_music_data(now_playing['artist'], now_playing['album'], now_playing['title'])
        sleep(10)

@server.route("/music/nowplaying")
def music_nowplaying():
    nowplaying = get_current_song()
    urls = nowplaying['album_art'].split('http://')
    album_art = 'http://' + urls[len(urls) - 1]
    response = { 'artist': nowplaying['artist'], 'album': nowplaying['album'], 'title': nowplaying['title'], 'album_art': album_art }
    return json.dumps(response)

@server.route("/music/pandora/stations/<pandora_email>")
def music_pandora_stations(pandora_email):
    user = get_pandora_user(pandora_email)
    stations = get_stations(user)
    return json.dumps(stations)

@server.route("/music/pandora/play/<station_code>")
def music_pandora_play(station_code):
    if True == play_pandora_station(station_code):
        return 'OK'
    else:
        return 'FAIL'

@server.route("/peggy/weather")
def peggy_weather():
    weather_thread = Thread(target=peggy_weather_loop)
    weather_thread.start()
    return "OK\r\n"
    
@server.route("/peggy/nowplaying")
def peggy_music():
    global music_on;
    if music_on == False:
        music_thread = Thread(target=peggy_music_loop)
        music_thread.start()
        return "OK"
    else:
        return "ALREADY RUNNING"

@server.route("/peggy/sleep")
def peggy_sleep():
    global sleep_on, weather_on, music_on
    if weather_on:
        weather_on = False
    if music_on:
        music_on = False
    if sleep_on == False:
        sleep_on = True

    set_display_mode(displayMode_Sleep)

    return "OK\r\n"

if __name__ == "__main__":
    server.debug = True
    server.run(host='0.0.0.0')
