from src.event import *
from src.textArea import *
import lib.bsgui as gui

class TextBox:
	def __init__(self, window, textBuffer):
		self.window = window
		self.className = "TextBox"
		self.name = "bsText"
		self.eventDispatcher = EventDispatcher()
		self.eventDispatcher.setHandler("keyPress", self.keyPressHandler)
		self.children = {"textArea": TextArea(window)}
		self.text = {} # Массив со строками которые остается просто нарисовать
					   # на экране
		self.textBuffer = textBuffer

	def keyPressHandler(self, params):
		self.children["textArea"].eventDispatcher.emit("keyPress")
		if params["key"] == "up":
			self.textBuffer.cursor.up(self.textBuffer)

		elif params["key"] == "down":
			self.textBuffer.cursor.down(self.textBuffer)

		elif params["key"] == "left":
			self.textBuffer.cursor.left(self.textBuffer)

		elif params["key"] == "right":
			self.textBuffer.cursor.right(self.textBuffer, True)

		elif params["key"] == "backspace":
			self.textBuffer.delSymbol()
			self.textBuffer.cursor.left(self.textBuffer)

		elif len(params["key"]) == 1:
			self.textBuffer.addSymbol(params["key"])
			self.textBuffer.cursor.right(self.textBuffer, False)
		self.window.updateWindow()

	def render(self, window, props, parentProps):
		self.text = props[4]
		gui.drawText(window, "My TextBox", 20, 20)
		gui.drawRectangle(window, 20, 20, 800, 300, "transparent", "#FF0000")
		self.children["textArea"].render(window, {
			"text": props[4],
			"cursor": self.textBuffer.cursor,
		}, props)
		# Scrollbar.render(window, self.widget["children"]["scrollbar"],
		# 	{}, props)
