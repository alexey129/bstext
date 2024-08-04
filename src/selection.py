import copy
from pyrsistent import pvector, pmap

import lib.bsgui as gui
from src.event import *

def SELsetCoordSelection(textBuffer, x1, y1, x2, y2):
	"""
	x1 и y1 - координаты первого символа(считаем в символах)
	x2 и y2 - координаты второго символа(считаем в символах)
	Берет координаты первого и последнего символа в выделении, и заполняет
	массив self.selectBoxes данными о выделении.
	"""
	selectBoxes = pvector()
	for count, i in enumerate(textBuffer.viewBufferCopy):
		# Если и начало и конец выделения находится на одной строке.
		#print(y1, y2, count)
		if y1 == count and y2 == count:
			selectBoxes = selectBoxes.append(pmap({
				"count": count,
				"start": x1,
				"end": x2,
			}))
	return selectBoxes

def SELaddSelectionRight(data, textBuffer, x2, y2):
	"""
	x2 и y2 - координаты символа справа, который будет концом выделения.
	Добавляем символ справа к выделению.
	"""
	#print(1, data)
	data = data.set("x2", x2)
	data = data.set("y2", y2)
	data = data.set("selectBoxes", SELsetCoordSelection(
		textBuffer, data["x1"], data["y1"], data["x2"], data["y2"]))
	#print(2, data)
	return data

class Selection:
	"""
	Это только представление выделения и отвечает только за рисование его на
	экране.
	"""
	def __init__(self, window, textBuffer):
		self.className = "Selection"
		self.name = "bsText"
		self.eventDispatcher = EventDispatcher()
		self.eventDispatcher.setHandler("keyPress", self.keyPressHandler)
		self.children = {}
		# Координаты символов и строк которые надо выделить.
		# Формат - номер строки на экране, первый символ, последний символ
		self.textBuffer = textBuffer

		self.data = pmap({
			# На какой строке от какого до какого символа выделено.
			"selectBoxes": pvector(),
			# Координаты начала выделения (в символах)
			"x1": 0,
			"y1": 0,
			# Координаты конца выделения (в символах)
			"x2": 0,
			"y2": 0,
		})

	def keyPressHandler(self):
		pass

	def render(self, window, props, parentProps):
		# Размеры курсора.
		w = 2
		h = 20

		# Верхний левый угол текстбокса.
		xstart = 20
		ystart = 50

		# Размеры одного символа.
		sw = 13
		sh = 20

		for i in self.data["selectBoxes"]:
			x = xstart + sw * i["start"]
			y = ystart + sh * i["count"]
			w = sw * i["end"] - i["start"]
			h = sh
			gui.drawRectangle(window, x, y, w, h, "transparent", "#FF0000")