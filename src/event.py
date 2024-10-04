from lib.bslib.func import *


class EventDispatcher:
	def __init__(self):
		self.events = {}

	def setHandler(self, name, func):
		self.events[name] = func

	def emit(self, name, params = None):
		func = self.events[name]
		if params is None:
			func()
		else:
			func(params)

def createEventDispatcher():
	return ()

def setHandler(disp, name, func):
	return disp + ((name, func),)

def emit(disp, name, params = None):
	func = getValTup(disp, name)
	if params is None:
		return func()
	else:
		return func(params)