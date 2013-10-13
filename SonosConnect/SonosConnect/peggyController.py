from peggy import *
from weather import *
from datetime import *
from time import sleep

def run():
    while(1):
        now = datetime.now()
        send_time(now.hour, now.minute)
        send_date(now.year - 2000, now.month, now.day)

        weather = get_current_conditions("98122")
        send_weather(weather['temperature'], weather['humidity'], weather['condition'])

        sleep(10)

run()
