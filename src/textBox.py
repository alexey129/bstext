from src.event import *
from src.textArea import *
from src.selection import *
import lib.bsgui as gui
from var_dump import var_dump

def keyRight(window, selfa, isShift, textBuffer):
	if isShift:
		textBuffer.addSelectionRight()
		if selfa.selection is None:
			selfa.selection = Selection(window, textBuffer)
			selfa.selection.data = selfa.selection.data.set(
				"x1", textBuffer.cursor.x)
			selfa.selection.data = selfa.selection.data.set(
				"y1", textBuffer.cursor.y)
			selfa.selection.data = selfa.selection.data.set(
				"x2", textBuffer.cursor.x)
			selfa.selection.data = selfa.selection.data.set(
				"y2", textBuffer.cursor.y)
			selfa.selection.data = selfa.selection.data.set("selectBoxes",
				SELsetCoordSelection(
				textBuffer,
				# Передаем координаты одного и того же символа потому что в
				# выделении пока нет символов.
				textBuffer.cursor.x,
				textBuffer.cursor.y,
				textBuffer.cursor.x,
				textBuffer.cursor.y))
		else:
			selfa.selection.data = SELaddSelectionRight(
				selfa.selection.data,
				textBuffer,
				textBuffer.cursor.x,
				textBuffer.cursor.y)
			print(selfa.selection.data["selectBoxes"])
	textBuffer.cursor.right(textBuffer, True)


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
		self.isShiftPressed = False

		self.selection = None

	def keyPressHandler(self, params):
		self.children["textArea"].eventDispatcher.emit("keyPress")
		if params["key"] == "up":
			self.textBuffer.cursor.up(self.textBuffer)

		elif params["key"] == "down":
			self.textBuffer.cursor.down(self.textBuffer)

		elif params["key"] == "left":
			if self.isShiftPressed:
				self.textBuffer.addSelectionLeft()
			self.textBuffer.cursor.left(self.textBuffer)

		elif params["key"] == "right":
			keyRight(self.window, self, self.isShiftPressed,
				self.textBuffer)

		elif params["key"] == "backspace":
			if (not(self.textBuffer.cursor.x == 0 and
				self.textBuffer.cursor.y == 0)):
					self.textBuffer.delSymbol()
					self.textBuffer.cursor.left(self.textBuffer)

		elif params["key"] == "mouseWheelUp":
			self.textBuffer.scrollUp()

		elif params["key"] == "mouseWheelDown":
			self.textBuffer.scrollDown()

		elif params["key"] == "shift":
			self.isShiftPressed = True

		elif params["key"] == "shiftRealize":
			self.isShiftPressed = False

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
		if self.selection is not None:
			self.selection.render(window, {}, props)
		# Scrollbar.render(window, self.widget["children"]["scrollbar"],
		# 	{}, props)
