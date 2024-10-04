# Функции для работы с виджетами.

from lib.bslib.func import *


def AbstractWidget():
	"""
	Возвращает абстрактный виджет
	"""
	return namedtuple("AbstractWidget", [
		"onPaint",
		"onKeyPress",
		"x",
		"y",
		"width",
		"height",
		"children",
	])

def newWidget(name, tpl):
	"""
	Создает новый виджет, отнаследованный от абстрактного.
	"""
	return namedtuple(name, AbstractWidget()._fields + tpl)

def iterChildrenWidget(widget):
	"""
	Возвращает итератор для перебора детей виджета.
	"""
	return itemsTuple(widget.children)

def drawChildren(widget, canvas):
	"""
	Рисует всех детей виджета, то есть вызывает у всех детей функцию onPaint.
	"""
	for key, value in iterChildrenWidget(widget):
		value.onPaint(value, canvas)

def keyPressChildren(widget, key):
	"""
	Нажимает клавишу у всех детей.
	"""
	upEvents = ()
	for name, child in iterChildrenWidget(widget):
		chandgedChild, upEv = child.onKeyPress(child, key)
		#print(child, upEv)
		upEvents = upEvents + upEv
		widget = setChild(widget, name, chandgedChild)
	return widget, upEvents

def addChild(widget, name, child):
	return widget._replace(children = widget.children + ((name, child),))

def setChild(widget, name, child):
	return widget._replace(children = setValTup(widget.children, name, child))

def getChild(widget, name):
	return getValTup(widget.children, name)