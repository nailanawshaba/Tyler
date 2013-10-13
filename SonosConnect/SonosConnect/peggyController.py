from peggy import *
from weather import *
from datetime import *
from time import sleep
from threading import Thread
from flask import Flask
from SonosConnect import connect, update_song_info

server = Flask(__name__)

weather_on = False
music_on = False
sleep_on = True

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

    connect()
    while(music_on):
        update_song_info()
        sleep(10)

@server.route("/peggy/weather")
def peggy_weather():
    weather_thread = Thread(target=peggy_weather_loop)
    weather_thread.start()
    return "OK\r\n"

@server.route("/peggy/music")
def peggy_music():
    music_thread = Thread(target=peggy_music_loop)
    music_thread.start()
    return "OK\r\n"

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
