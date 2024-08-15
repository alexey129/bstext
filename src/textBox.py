from src.event import *
from src.textArea import *
from src.selection import *
from src.textBuffer import *
import lib.bsgui as gui
from var_dump import var_dump

def getLeftSideStr(string, index):
	"""
	Возвращает левую часть строки считая от позиции index.
	"""
	text = string.text
	if index < len(text):
		return text[:index]
	else:
		return text

def getRightSideStr(string, index):
	"""
	Возвращает правую часть строки считая от позиции index.
	"""
	text = string.text
	if index < len(text):
		return text[index:]
	else:
		return text

def getLineAboveCursor(y, screenLines, lineAbove, lineUnder):
	"""
	Возвращает строку которая находится выше курсора.
	"""
	if y < 0 or y >= len(screenLines):
		raise Exception("Координата y не подходит")
	if y == 0:
		if lineAbove == None:
			return ViewLine()
		else:
			return lineAbove
	else:
		return screenLines[y - 1]

def getLineUnderCursor(y, screenLines, lineAbove, lineUnder):
	"""
	Возвращает строку которая находится ниже курсора.
	"""
	if y < 0 or y > len(screenLines):
		raise Exception("Координата y не подходит")
	elif y == len(screenLines) - 1:
		if lineUnder == None:
			return ViewLine()
		else:
			return lineUnder
	else:
		return screenLines[y + 1]

def getLineCursor(y, screenLines):
	"""
	Возвращает строку на которой находится курсор.
	"""
	return screenLines[y]


def whereAndHowMuch(key, cursor, screenLines, lineAbove, lineUnder):
	"""
	Куда и на сколько символов мы сдвинемся если нажмем на клавишу перемещения
	курсора.
	"""
	where = key
	howMuch = 0
	if where in ("left", "right"):
		howMuch = 1
	else:
		if where == "up":
			howMuch = len(getLeftSideStr(
				getLineCursor(cursor.y, screenLines), cursor.x) +
				getRightSideStr(getLineAboveCursor(
					cursor.y, screenLines, lineAbove, lineUnder), cursor.x)
				)
		if where == "down":
			howMuch = len(getRightSideStr(
				getLineCursor(cursor.y, screenLines), cursor.x) +
				getLeftSideStr(getLineUnderCursor(
					cursor.y, screenLines, lineAbove, lineUnder), cursor.x))
	return (where, howMuch)

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

	def keyPressHandler(self, params):
		cursor = self.textBuffer.cursor
		self.children["textArea"].eventDispatcher.emit("keyPress")

		if (params["key"] == "up" or
		params["key"] == "down" or
		params["key"] == "left" or
		params["key"] == "right"):
			if self.isShiftPressed:
				aaa = whereAndHowMuch(
					params["key"],
					cursor,
					self.textBuffer.viewBufferCopy,
					self.textBuffer.lineAboveScreen,
					self.textBuffer.lineUnderScreen,
					)
				if aaa[0] in ("left", "up"):
					aaa = ("left", aaa[1])
				elif aaa[0] in ("right", "down"):
					aaa = ("right", aaa[1])
				self.textBuffer.changeSelection(aaa)
			else:
				self.textBuffer.selection = None
				self.textBuffer.selectionScreen = None
			self.textBuffer.cursor.toDirect(params["key"], self.textBuffer)

		elif params["key"] == "backspace":
			if self.textBuffer.selection is None:
				if (not(cursor.x == 0 and
					cursor.y == 0)):
						self.textBuffer.delSymbol()
						cursor.left(self.textBuffer)
			else:
				# Удаляем то что было выделено.
				deleteTextSelection(self.textBuffer, self.textBuffer.selectionScreen)
				self.textBuffer.selection = None
				self.textBuffer.selectionScreen = None

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
			cursor.right(self.textBuffer, False)

		self.window.updateWindow()

	def render(self, window, props, parentProps):
		self.text = props[4]
		gui.drawText(window, "My TextBox", 20, 20)
		gui.drawRectangle(window, 20, 20, 800, 300, "transparent", "#FF0000")
		self.children["textArea"].render(window, {
			"text": props[4],
			"cursor": self.textBuffer.cursor,
		}, props)
		if self.textBuffer.selection is not None:
			selectionRender(window,
				{"coords": self.textBuffer.selectionScreen,
				"textBuffer": self.textBuffer.viewBufferCopy,
				"cursor": self.textBuffer.cursor,
				"selection": self.textBuffer.selection}, props)
