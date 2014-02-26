from ouimeaux.environment import Environment

# TODO:
#    - lacks a way to clear the device cache

class WemoController:
    _env = None

    def _on_switch(self, switch):
	print "Light Switch found: ", switch.name

    def _on_motion(self, motion):
	print "Motion Sensor found: ", motion.name

    def connect(self):
	self._env = Environment(self._on_switch, self._on_motion)
	try:
	    self._env.start()
	except TypeError:
	    print "Start error"
	try:
	    self._env.discover(seconds=3)
	except TypeError:
	    print "Discovery error"

    def find_switches(self):
	result = []
	switches = self._env.list_switches()
	print "Found " + str(len(switches))
	print switches
	for s in switches:
	    print "Found " + s
	    result.append({ "name" : s, "state" : self._env.get_switch(s).get_state() }) 
	return result

    def switch_on(self, switch_name):
	switch = self._env.get_switch(switch_name)
	switch.on()

    def switch_off(self, switch_name):
	switch = self._env.get_switch(switch_name)
	switch.off()

    def switch_state(self, switch_name):
	switch = self._env.get_switch(switch_name)
	return switch.get_state()
