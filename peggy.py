from xbee import XBee
from serial import Serial
from struct import *
from threading import Thread

import time
import datetime
import weather
import sonos

PEGGY_ADDRESS = '\xE0\x03'
SERIAL_PORT = "/dev/ttyAMA0"
BAUD_RATE = 9600

cmd_SwitchDisplayMode = 0
cmd_SetDate = 1
cmd_SetTime = 2
cmd_SetWeather = 3
cmd_SetMusicData = 4

displayMode_Sleep = 0
displayMode_Weather = 1
displayMode_Sonos = 2

weather_conditions = {
    'Sunny' : 0,
    'Rainy' : 1,
    'Cloudy' : 2,
    'Mostly Cloudy' : 2,
    'Foggy' : 3,
    'Snowy' : 4,
    'Partly Cloudy': 5
}

class PeggyController:
    _state = displayMode_Sleep
    _now_playing = None

    def show_music(self):
	set_display_mode(displayMode_Sonos)
        music_thread = Thread(target=self._show_music_thread)
        music_thread.start()

    def show_weather(self):
        self._set_display_mode(displayMode_Weather)
	weather_thread = Thread(target=peggy_weather_loop)
	weather_thread.start()

    def sleep(self):
        set_display_mode(displayMode_Sleep)

    def _show_music_thread(self):
	sonos.connect()
	while(self._state == displayMode_Sonos):
	    tmp = sonos.get_current_song()
	    if not is_same_song(self._now_playing, tmp):     
		self._now_playing = tmp
		self._send_music_data()
	    time.sleep(10)
    
    def _show_weather_thread(self):
        while(self._state == displayMode_Weather):
            now = datetime.now()
            self._send_time(now.hour, now.minute)
            self._send_date(now.year - 2000, now.month, now.day)

            current_weather = weather.get_current_conditions("98122")
            self._send_weather(weather['temperature'], weather['humidity'], weather['condition'])
            time.sleep(10)

    def _is_same_song(self, song1, song2):
        result = False
	if song1 != None and song2 != None:
	    identicalArtists = song1['artist'] == song2['artist']
	    identicalTitles = song1['title'] == song2['title']
	    identicalAlbums = song1['album'] == song2['album']
            if identicalArtists and identicalTitles and identicalAlbums:
	        result = True
	return result

    def _set_display_mode(self, displayMode):
        self._state = displayMode
	data = pack('BB', cmd_SwitchDisplayMode, displayMode)
	return self._send_command(data)

    def _send_time(self, hours, minutes):
	data = pack('BBBBB', cmd_SetTime, hours / 10, hours % 10, minutes / 10, minutes % 10)
	return self._send_command(data)

    def _send_date(self, year, month, day):
	data = pack('BBBBBBB', cmd_SetDate, day / 10, day % 10, month / 10, month % 10, year / 10, year % 10)
	return self._send_command(data)
	
    def _send_weather(self, temperature, humidity, condition):
	data = pack('BBBB', cmd_SetWeather, temperature, humidity, int(weather_conditions[condition]))
	return self._send_command(data)

    def _send_music_data(self):
        artist_length = len(self._now_playing['artist'])
        album_length = len(self._now_playing['album'])
        title_length = len(self._now_playing['title'])
	
        fmt = 'BBBB'+ str(artist_length + 1) + 's' + str(album_length + 1) + 's' + str(title_length + 1) + 's'
	print fmt
	data = pack(fmt, cmd_SetMusicData, artist_length + 1, album_length + 1, title_length + 1, self._now_playing['artist'] + '\0', self._now_playing['album'] + '\0', self._now_playing['title'] + '\0');
	print "Now Playing: {0} - {1} ({2})".format(self._now_playing['artist'], self._now_playing['title'], self._now_playing['album'])
	return self._send_command(data)

    def _send_command(self, data):
	ser = Serial(SERIAL_PORT, BAUD_RATE)
	xbee = XBee(ser)
	try:
	    xbee.tx(dest_addr=PEGGY_ADDRESS, data=data)
	    ser.close()
	    return True
	except:
	    ser.close()
	    return False
