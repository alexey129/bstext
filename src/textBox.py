from src.event import *
from src.textArea import *
from src.selection import *
from src.textBuffer import *
import src.textNumber as TextNumber
from config.viewConfig import viewConfig
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

def keyPressHandler(params):
	textbox = params["textBox"]
	cursor = textbox.textBuffer.cursor
	textbox.children["textArea"].eventDispatcher.emit("keyPress")

	if (params["key"] == "up" or
	params["key"] == "down" or
	params["key"] == "left" or
	params["key"] == "right"):
		if textbox.isShiftPressed:
			aaa = whereAndHowMuch(
				params["key"],
				cursor,
				textbox.textBuffer.viewBufferCopy,
				textbox.textBuffer.lineAboveScreen,
				textbox.textBuffer.lineUnderScreen,
				)
			if aaa[0] in ("left", "up"):
				aaa = ("left", aaa[1])
			elif aaa[0] in ("right", "down"):
				aaa = ("right", aaa[1])
			textbox.textBuffer.changeSelection(aaa)
		else:
			textbox.textBuffer.selection = None
			textbox.textBuffer.selectionScreen = None
		textbox.textBuffer.cursor.toDirect(params["key"], textbox.textBuffer)

	elif params["key"] == "backspace":
		if textbox.textBuffer.selection is None:
			if (not(cursor.x == 0 and
				cursor.y == 0)):
					textbox.textBuffer.delSymbol()
					cursor.left(textbox.textBuffer)
		else:
			# Удаляем то что было выделено.
			deleteTextSelection(textbox.textBuffer, textbox.textBuffer.selection)
			textbox.textBuffer.selection = None
			textbox.textBuffer.selectionScreen = None

	elif params["key"] == "mouseWheelUp":
		textbox.textBuffer.scrollUp()

	elif params["key"] == "mouseWheelDown":
		textbox.textBuffer.scrollDown()

	elif params["key"] == "shift":
		textbox.isShiftPressed = True

	elif params["key"] == "shiftRealize":
		textbox.isShiftPressed = False

	elif len(params["key"]) == 1:
		textbox.textBuffer.addSymbol(params["key"])
		cursor.right(textbox.textBuffer, False)

	textbox.window.updateWindow()

class TextBox:
	def __init__(self, window, textBuffer):
		self.window = window
		self.className = "TextBox"
		self.name = "bsText"
		self.eventDispatcher = EventDispatcher()
		self.eventDispatcher.setHandler("keyPress", keyPressHandler)
		self.children = {"textArea": TextArea(window)}
		self.textBuffer = textBuffer
		self.isShiftPressed = False

	def render(self, window, props, parentProps):
		gui.drawText(window, "My TextBox", 20, 20)
		gui.drawRectangle(window, 20, 20, 800, 300,
			viewConfig["textBoxBackgroundColor"])
		self.children["textArea"].render(window, {
			"text": props[4],
			"cursor": self.textBuffer.cursor,
		}, props)
		TextNumber.render(window, {
			"text": props[4],
			"cursor": self.textBuffer.cursor,
		}, props)
		if self.textBuffer.selection is not None:
			selectionRender(window,
				{"coords": self.textBuffer.selectionScreen,
				"textBuffer": self.textBuffer.viewBufferCopy,
				"cursor": self.textBuffer.cursor,
				"selection": self.textBuffer.selection}, props)
