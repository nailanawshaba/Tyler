from pywapi import get_weather_from_weather_com

def get_current_temperature(location):
    result = get_weather_from_weather_com(location)
    return result

def get_current_conditions(location):
    result = get_weather_from_weather_com(location)
    retval = { 'condition' : result['current_conditions']['text'], 'temperature' : int(result['current_conditions']['temperature']), 'humidity' : int(result['current_conditions']['humidity'])}
    return retval
