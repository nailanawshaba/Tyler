# heavily copied from https://github.com/rahims/SoCo/pull/35/files#diff-73be93b9dad425d26a3e41d2cde306b6L-1 - original (and much more complete) work by Scott G. Waters.
import requests
import xml.etree.cElementTree as XML

def get_pandora_user(email):
    response = requests.get("http://www.pandora.com/services/ajax/?method=authenticate.emailToWebname&email=" + pandora_email)
    return response['results']['webname']

def get_stations(username):
    response = requests.get('http://feeds.pandora.com/feeds/people/' + username + '/stations.xml')
    dom = XML.fromstring(response.content)
    stations = {}

    for s in dom.findall(".//item"):
        title = s.find("title").text
        code = s.find('.//{http://www.pandora.com/rss/1.0/modules/pandora/}stationCode').text
        stations[title] = code.strip("sh")

    return stations