import src.event as event
import lib.bsgui as gui
from collections import namedtuple
from lib.bslib.func import *
from var_dump import var_dump
import src.widget as W

def keyPressHandler(cursor, key):
	return cursor

def render(cursor, canvas):
	# Размеры курсора.
	w = 2
	h = 20

	# Верхний левый угол текстбокса.
	xstart = 20
	ystart = 50

	# Размеры одного символа.
	sw = 13
	sh = 20

	curs = cursor
	# Верхний левый угол курсора.
	xc = xstart + curs.x*sw
	yc = ystart + curs.y*sh
	gui.drawRectangle(canvas, xc, yc, w, h, "transparent", "#FF0000")
	
	W.drawChildren(cursor, canvas)

Cursor = W.newWidget("Cursor", ())

def createCursor(parent, name, x, y, width, height):
	"""
	Добавляет новый виджет к родителю.
	"""
	cursor = Cursor(
		onPaint = render,
		onKeyPress = keyPressHandler,
		x = x,
		y = y,
		width = width,
		height = height,
		children = (),
	)
	return cursor