from src.event import *
import lib.bsgui as gui

from src.cursor import *

class TextArea:
	def __init__(self, window):
		self.className = "TextArea"
		self.name = "bsText"
		self.eventDispatcher = EventDispatcher()
		self.eventDispatcher.setHandler("keyPress", self.keyPressHandler)
		self.children = {"cursor": Cursor(window)}

	def keyPressHandler(self):
		pass

	def render(self, window, props, parentProps):
		gui.drawText(window, "My TextArea", 20, 20)
		gui.drawRectangle(window, 20, 20, 800, 300, "transparent", "#FF0000")
		self.children["cursor"].render(window, {
			"cursor": props["cursor"],
		}, props)
		count = 50
		for i in props["text"]:
			gui.drawText(window, i.text, 20, count)
			count += 20
