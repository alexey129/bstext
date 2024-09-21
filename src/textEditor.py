from collections import namedtuple
from var_dump import var_dump
import src.event as event
import src.textBox as tBox
from src.textBuffer import *
import lib.bsgui as gui
from lib.bslib.func import *
from lib.bslib.log import *
import src.widget as W

TextEditor = W.newWidget("TextEditor", (
	"textBuffer",
))

def keyPressHandler(textEditor, key):
	return W.keyPressChildren(textEditor, key)
	# Тут смысл был в том чтоб в params еще передать родителя.
	# params["textBox"] = self.children["textBox"]
	# self.children["textBox"].eventDispatcher.emit("keyPress", params)

def render(textEditor):
	gui.drawRectangle(
		textEditor.window,
		textEditor.x,
		textEditor.y,
		textEditor.width,
		textEditor.height,
		"transparent", "#FF0000")
	W.drawChildren(textEditor)

def createTextEditor(window, name, x, y, width, height):
	"""
	Добавляет новый виджет к родителю.
	"""
	textEditor = TextEditor(
		onPaint = render,
		onKeyPress = keyPressHandler,
		x = x,
		y = y,
		width = width,
		height = height,
		children = (),
		window = window,
		textBuffer = TextBuffer(),
	)

	textEditor.textBuffer.setTextFromFile("assets/text.txt")

	tb = tBox.createTextBox(textEditor, "textBox", 0, 0, 800, 400)
	tb = tb._replace(textBuffer = textEditor.textBuffer)
	tb = tBox.setTextBuffer(tb, textEditor.textBuffer)
	#var_dump(tb)
	textEditor = W.addChild(textEditor, "textBox", tb)
	return textEditor