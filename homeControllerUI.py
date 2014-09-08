#!/usr/bin/python

import sys

from Tkinter import Tk, Frame, Button, Label, BOTH, RIGHT, X
from homeControllerClient import HomeControllerClient

class MainWindow(Frame):
	buttons = []

	def __init__(self, parent, serverIP):
		Frame.__init__(self, parent, bg="black")
		self.parent = parent
		self.controller = HomeControllerClient(serverIP)
		self.initUI()

	def listSwitches(self):
		count = -1
		while (count == -1):
			try:
				switches = self.controller.getSwitches()
				count = len(switches)
			except:
				count = -1

		for b in self.buttons:
			b.destroy()

		for k in switches.keys():

			bgColor = "red"
			if(switches[k] == 1):
				bgColor = "green"

			btn = Button(self, text=k, bg=bgColor, command=self.generateCallback(k))
			self.buttons.append(btn)
			btn.pack(fill=X, padx=5, pady=5)

	def generateCallback(self, name):
		def callback():
			self.toggle(name)
		return callback
		
	def toggle(self, name):
		self.controller.toggleSwitch(name)
		self.listSwitches()

	def initUI(self):
		self.parent.title("Main Window")
		self.pack(fill=BOTH, expand=1)
		lbl = Label(self, text="Home Controller", fg="white", bg="black")
		lbl.pack(fill=X, padx=5, pady=5)
		self.listSwitches()


def main():
	if (len(sys.argv) != 2):
		print "Please specify IP or hostname of the server"
		exit()

	root = Tk()
	root.overrideredirect(1)
	root.geometry("320x240+0+0")
	app = MainWindow(root, sys.argv[1])
	root.mainloop()

if __name__ == '__main__':
	main()