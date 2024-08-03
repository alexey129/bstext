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