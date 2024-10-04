import lib.bsgui as gui
import src.textBox as tBox
import src.menu as Mn
import src.widget as W
from src.textBuffer import *

TextEditor = W.newWidget("TextEditor", (
	"textBuffer",
))

def keyPressHandler(textEditor, key):
	a, b = W.keyPressChildren(textEditor, key)
	print(b, "qqqqqqq")
	return a
	# Тут смысл был в том чтоб в params еще передать родителя.
	# params["textBox"] = self.children["textBox"]
	# self.children["textBox"].eventDispatcher.emit("keyPress", params)

def render(textEditor, canvas):
	gui.drawRectangle(
		canvas,
		textEditor.x,
		textEditor.y,
		textEditor.width,
		textEditor.height,
		"transparent", "#FF0000")
	W.drawChildren(textEditor, canvas)

def createTextEditor(name, x, y, width, height):
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
		textBuffer = TextBuffer(),
	)

	textEditor.textBuffer.setTextFromFile("assets/text.txt")

	tb = tBox.createTextBox(textEditor, "textBox",
		textEditor.x, 20, textEditor.width, textEditor.height - 20)
	menu = Mn.createMenu("menu",
		textEditor.x, textEditor.y, textEditor.width, 20)
	tb = tb._replace(textBuffer = textEditor.textBuffer)
	tb = tBox.setTextBuffer(tb, textEditor.textBuffer)
	#var_dump(tb)
	textEditor = W.addChild(textEditor, "textBox", tb)
	textEditor = W.addChild(textEditor, "menu", menu)
	return textEditor