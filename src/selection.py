import copy
import numbers
from pyrsistent import pvector, pmap

import lib.bsgui as gui
from src.event import *

# Мы должны сначала установить координаты в data, а потом по ним создавать
# selectBoxes.

def getSelectionBoxes(selectionRangeCoord, textWidth, lineCount):
	"""
	Берет координаты выделения и возвращает массив с прямоугольниками которые
	надо нарисовать на экране.
	"""
	x1, y1, x2, y2 = selectionRangeCoord

	def createBox(i):
		if y1 == i == y2:
			return pmap({"count": i, "start": x1, "end": x2})
		elif y1 == i:
			return pmap({"count": i, "start": x1, "end": text_width})
		elif y2 == i:
			return pmap({"count": i, "start": 0, "end": x2})
		elif y1 < i < y2:
			return pmap({"count": i, "start": 0, "end": text_width})
		else:
			return None

	return pvector(filter(None, map(createBox, range(lineCount))))


def selectionRender(window, props, parentProps):
	# Размеры курсора.
	w = 2
	h = 20

	# Верхний левый угол текстбокса.
	xstart = 20
	ystart = 50

	# Размеры одного символа.
	sw = 13
	sh = 20

	for i in getSelectionBoxes(props["coords"], 50, 10):
		# Проблема в этом коде:
		x = xstart + sw * i["start"]
		y = ystart + sh * i["count"]
		w = sw * (i["end"] - i["start"])
		h = sh
		# -----------------------
		gui.drawRectangle(window, x, y, w, h, "transparent", "#FF0000")

