from src.event import *
from src.textBox import *
from src.textBuffer import *
import lib.bsgui as gui

class TextEditor:
	def __init__(self, window):
		self.className = "TextEditor"
		self.name = "bsText"
		self.eventDispatcher = EventDispatcher()
		self.eventDispatcher.setHandler("keyPress", self.keyPressHandler)
		self.textBuffer = TextBuffer()
		self.textBuffer.setTextFromFile("assets/text.txt")
		self.children = {"textBox": TextBox(window, self.textBuffer)}

	def keyPressHandler(self, params):
		self.children["textBox"].eventDispatcher.emit("keyPress", params)
	# Эта функция должна изменять дерево виджетов. То есть вставлять созданные
	# виджеты в массив children. Нет, уже не должна.
	# Родительские пропсы нужны чтоб рисовать относительно родителя.
	def render(self, window, props, parentProps):
		gui.drawText(window, "My Text Editor", 0, 10)
		gui.drawRectangle(window, props["x"], props["y"],
			props["width"], props["height"], "transparent", "#FF0000")
		self.children["textBox"].render(window, [20,20,800,300,
			self.textBuffer.getViewText()], props)