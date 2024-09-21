import src.event as event
import lib.bsgui as gui
from var_dump import var_dump
from collections import namedtuple
from lib.bslib.func import *
import src.widget as W

import src.cursor as cur

def setTextBuffer(textArea, textBuffer):
	return textArea._replace(textBuffer = textBuffer)

def setCursor(textArea, cursor):
	return textArea._replace(cursor = cursor)

def keyPressHandler(textArea, key):
	cur = W.getChild(textArea, "cursor")
	cur = cur._replace(x = textArea.cursor.x, y = textArea.cursor.y)
	textArea = W.setChild(textArea, "cursor", cur)
	return textArea

def drawTextBuffer(window, textBuffer):
	if textBuffer is None:
		raise Exception("TextBuffer равен None")
	count = 50
	for i in textBuffer:
		gui.drawText(window, i.text, 20, count)
		count += 20

def render(textArea):
	drawTextBuffer(textArea.window, textArea.textBuffer)
	#gui.drawText(window, "My TextArea", 20, 20)
	#gui.drawRectangle(window, 20, 20, 800, 300, "transparent", "#FF0000")
	W.drawChildren(textArea)
	# self.children["cursor"].render(window, {
	# 	"cursor": props["cursor"],
	# }, props)

TextArea = W.newWidget("TextArea", (
	"textBuffer",
	"cursor",
))

def createTextArea(parent, name, x, y, width, height):
	"""
	Добавляет новый виджет к родителю.
	"""
	textArea = TextArea(
		onPaint = render,
		onKeyPress = keyPressHandler,
		x = x,
		y = y,
		width = width,
		height = height,
		textBuffer = None,
		children = (),
		window = parent.window,
		cursor = None
	)

	cursor = cur.createCursor(textArea, "textNumber", 0, 0, 20, 400)
	textArea = W.addChild(textArea, "cursor", cursor)

	return textArea