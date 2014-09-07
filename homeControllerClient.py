#!/usr/bin/python

import urllib
import urllib2
import json

class HomeControllerClient:
	switchList = dict()

	def __init__(self, serverIP):
		self.serverAddress = "http://" + serverIP + ":5000/"

	def getSwitches(self):
		req = urllib2.Request(self.serverAddress + "wemo/list")
		resp = urllib2.urlopen(req)
		responseBody = resp.read()
		jsonResponse = json.loads(responseBody)
		for s in jsonResponse:
			self.switchList[str(s['name'])] = s['state']

		return self.switchList

	def toggleSwitch(self, switchName):
		print "TOGGLE: " + switchName
		order = "on"
		if(self.switchList[switchName] == 1):
			order = "off"
		req = urllib2.Request(self.serverAddress + "wemo/" + order  + "/" + urllib.quote(switchName))
		resp = urllib2.urlopen(req)
