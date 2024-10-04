import lib.bsgui as gui
import src.textBox as tBox
import src.widget as W
from src.textBuffer import *
from collections import namedtuple

def clickOneButton():
	print("clickOneButton")

MenuButton = namedtuple("MenuButton", (
	"name",
	"action",
	"children",
))

Menu = W.newWidget("Menu", (
	"buttons",
))

def getCoordFromKey(key):
	coord = key.split("_")
	return (int(coord[1]), int(coord[2]))

def keyPressHandler(menu, key):
	upEvents = None
	if key.startswith("mouseLeft"):
		x, y = getCoordFromKey(key)
		count = 0
		for i in menu.buttons:
			lenName = len(i.name) * 13
			ax = menu.x + count
			ay = menu.y
			bx = menu.x + count + lenName
			by = menu.y + menu.height
			if (ax < x < bx) and (ay < y < by):
				if i.action is not None:
					i.action()
			count += lenName
		upEvents = ("menuButton",)
	return menu, upEvents

def render(menu, canvas):
	gui.drawRectangle(
		canvas,
		menu.x,
		menu.y,
		menu.width,
		menu.height,
		"transparent", "#FF0000")
	count = 0
	for i in menu.buttons:
		lenName = len(i.name) * 13
		gui.drawRectangle(
			canvas,
			menu.x + count,
			menu.y,
			lenName,
			menu.height,
			"transparent", "#FF0000")
		gui.drawText(canvas, i.name, menu.x + count, menu.y, "#103524")
		count += lenName
	W.drawChildren(menu, canvas)

def createMenu(name, x, y, width, height):
	"""
	Добавляет новый виджет к родителю.
	"""
	menu = Menu(
		onPaint = render,
		onKeyPress = keyPressHandler,
		x = x,
		y = y,
		width = width,
		height = height,
		children = (),
		buttons = (),
	)
	menu = menu._replace(buttons = (
		MenuButton(name = "wqr", action = clickOneButton, children = None),
		MenuButton(name = "4t3", action = None, children = None),
		MenuButton(name = "ggg3", action = None, children = None),
	))

	return menu