import src.event as event
import src.textArea as tArea
from src.selection import *
from src.textBuffer import *
import src.textNumber as TextNumber
from config.viewConfig import viewConfig
import lib.bsgui as gui
from var_dump import var_dump
from collections import namedtuple
from lib.bslib.log import *
import src.widget as W

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

def keyPressHandler(textbox, key):
	textBuffer = textbox.textBuffer
	#textbox = params["textBox"] #getValTup(params, "")
	cursor = textBuffer.cursor
	#textbox.children["textArea"].eventDispatcher.emit("keyPress")

	if key in ("up", "down", "left", "right"):
		if textbox.isShiftPressed:
			aaa = whereAndHowMuch(
				key,
				cursor,
				textBuffer.viewBufferCopy,
				textBuffer.lineAboveScreen,
				textBuffer.lineUnderScreen,
				)
			if aaa[0] in ("left", "up"):
				aaa = ("left", aaa[1])
			elif aaa[0] in ("right", "down"):
				aaa = ("right", aaa[1])
			textBuffer.changeSelection(aaa)
		else:
			textBuffer.selection = None
			textBuffer.selectionScreen = None
		textBuffer.cursor.toDirect(
			key, textBuffer)

	elif key == "backspace":
		if textBuffer.selection is None:
			if (not(cursor.x == 0 and
				cursor.y == 0)):
					textBuffer.delSymbol()
					cursor.left(textBuffer)
		else:
			# Удаляем то что было выделено.
			deleteTextSelection(
				textBuffer, textBuffer.selection)
			textBuffer.selection = None
			textBuffer.selectionScreen = None

	elif key == "mouseWheelUp":
		textBuffer.scrollUp()

	elif key == "mouseWheelDown":
		textBuffer.scrollDown()

	elif key == "shift":
		textbox = textbox._replace(isShiftPressed = True)

	elif key == "shiftRealize":
		textbox = textbox._replace(isShiftPressed = False)

	elif len(key) == 1:
		textBuffer.addSymbol(key)
		cursor.right(textBuffer, False)

	textbox = setTextBuffer(textbox, textBuffer)

	ta = W.getChild(textbox, "textArea")
	ta = tArea.setCursor(ta, cursor)
	textbox = W.setChild(textbox, "textArea", ta)

	textbox = W.keyPressChildren(textbox, key)
	return textbox
	#textbox.window.updateWindow()

def render(textBox):
	gui.drawRectangle(
		textBox.window,
		textBox.x,
		textBox.y,
		textBox.width,
		textBox.height,
		viewConfig["textBoxBackgroundColor"])

	if textBox.textBuffer.selection is not None:
		selectionRender(
			textBox.window,
			textBox.textBuffer.selectionScreen,
			textBox.textBuffer.viewBufferCopy,
			textBox.textBuffer.cursor,
			textBox.textBuffer.selection)
	W.drawChildren(textBox)

def setTextBuffer(textBox, textBuffer):
	textBox = textBox._replace(textBuffer = textBuffer)
	vbc = textBuffer.getViewText()
	ta = getValTup(textBox.children, "textArea")
	ta = tArea.setTextBuffer(ta, vbc)
	tn = getValTup(textBox.children, "textNumber")
	tn = TextNumber.setTextBuffer(tn, vbc)
	textBox = textBox._replace(children = (("textArea",ta), ("textNumber",tn)) )
	return textBox

TextBox = W.newWidget("TextBox", (
	"textBuffer",
	"isShiftPressed",
))

def createTextBox(parent, name, x, y, width, height):
	"""
	Добавляет новый виджет к родителю.
	"""
	textBox = TextBox(
		onPaint = render,
		onKeyPress = keyPressHandler,
		x = x,
		y = y,
		width = width,
		height = height,
		isShiftPressed = False,
		children = (),
		window = parent.window,
		textBuffer = None
	)

	ta = tArea.createTextArea(textBox, "textArea", 20, 0, 800, 400)
	#ta = tArea.setTextBuffer(ta, textBox.textBuffer)
	tn = TextNumber.createTextNumber(textBox, "textNumber", 0, 0, 20, 400)
	#tn = TextNumber.setTextBuffer(tn, textBox.textBuffer)

	textBox = W.addChild(textBox, "textArea", ta)
	textBox = W.addChild(textBox, "textNumber", tn)

	return textBox