import lib.bsgui as gui
import src.event as event
from config.viewConfig import viewConfig
from lib.bslib.func import *
import src.widget as W

def setTextBuffer(textNumber, textBuffer):
	return textNumber._replace(textBuffer = textBuffer)

def keyPressHandler(textNumber, key):
	return textNumber

def drawTextBuffer(window, textBuffer):
	if textBuffer is None:
		raise Exception("TextBuffer равен None")

	count = 50
	num = None
	for i in textBuffer:
		if num != i.absNum:
			gui.drawText(window, str(i.absNum), 5, count,
				viewConfig["textBoxLineNumberColor"])
			num = i.absNum
		count += 20

def render(textNumber):
	#gui.drawText(window, "My TextArea", 20, 20)
	#gui.drawRectangle(window, 20, 20, 800, 300, "transparent", "#FF0000")
	drawTextBuffer(textNumber.window, textNumber.textBuffer)
	W.drawChildren(textNumber)

TextNumber = W.newWidget("TextNumber", (
	"textBuffer",
))

def createTextNumber(parent, name, x, y, width, height):
	"""
	Добавляет новый виджет к родителю.
	"""
	textNumber = TextNumber(
		onPaint = render,
		onKeyPress = keyPressHandler,
		x = x,
		y = y,
		width = width,
		height = height,
		textBuffer = None,
		children = (),
		window = parent.window,
	)

	return textNumber