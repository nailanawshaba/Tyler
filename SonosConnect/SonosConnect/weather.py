from pywapi import get_weather_from_weather_com

def get_current_temperature(location):
    result = get_weather_from_weather_com(location)
    return result

def get_current_conditions(location):
    result = get_weather_from_weather_com(location);
    return result['current_conditions']['text'] + ": " + result['current_conditions']['temperature'] + "C - " + result['current_conditions']['humidity'] + "%"

print get_current_conditions("98122")