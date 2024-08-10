import copy
import numbers
from pyrsistent import pvector, pmap

import lib.bsgui as gui
from src.event import *

def expandDataCoord(selectionRangeCoord, cursorCoord, direct):
	"""
	Расширяет выделение до какого то символа. Возвращает новое выделение.
	"""
	sx1, sy1, sx2, sy2 = selectionRangeCoord
	cx, cy = cursorCoord
	# Расширяем выделение.
	# Идем влево/вверх.
	if ((cx < sx1 and cy == sy1) or cy < sy1):
		return (cx, cy, sx2, sy2)
	# Идем вправо/вниз.
	elif ((cx > sx2 and cy == sy2) or cy > sy2):
		return (sx1, sy1, cx, cy)

	# Сужаем выделение.
	# Идем влево/вверх.
	elif ((direct == "left" or direct == "up") and
		(((cx == sx2 - 1) and (cy == sy2)) or (sy1 <= cy < sy2))):
			return (sx1, sy1, cx, cy)
	# Идем вправо/вниз.
	elif ((direct == "right" or direct == "down") and
		(((cx == sx1 + 1) and (cy == sy1)) or (sy1 < cy <= sy2))):
			return (cx, cy, sx2, sy2)
	# Это тут скорее чисто на всякий случай.
	else:
		return (sx1, sy1, sx2, sy2)

def setSelectionRange(selectionRangeCoord, cursor, direct):
	"""
	Принимает текущее выделение и текущую координату курсора, и возвращает
	новые координа выделения.
	direct - направление в котором мы двигаемся стрелками.
	"""
	if selectionRangeCoord is None:
		# -1 тут нужен чтоб создавать выделение сразу когда впервые сдвинулись
		# вправо.
		return (cursor.x - 1, cursor.y, cursor.x, cursor.y)
	else:
		return expandDataCoord(selectionRangeCoord, (cursor.x, cursor.y),
			direct)

# Мы должны сначала установить координаты в data, а потом по ним создавать
# selectBoxes.

def getSelectionBoxes(selectionRangeCoord, textWidth, lineCount, textBuffer):
	"""
	Берет координаты выделения и возвращает массив с прямоугольниками которые
	надо нарисовать на экране.
	"""
	x1, y1, x2, y2 = selectionRangeCoord

	def createBox(i):
		if y1 == i == y2:
			return pmap({"count": i, "start": x1, "end": x2})
		elif y1 == i:
			return pmap({"count": i, "start": x1, "end": textBuffer[i].length})
		elif y2 == i:
			return pmap({"count": i, "start": 0, "end": x2})
		elif y1 < i < y2:
			return pmap({"count": i, "start": 0, "end": textBuffer[i].length})
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

	for i in getSelectionBoxes(props["coords"], 50, 10, props["textBuffer"]):
		# Проблема в этом коде:
		x = xstart + sw * i["start"]
		y = ystart + sh * i["count"]
		w = sw * (i["end"] - i["start"])
		h = sh
		# -----------------------
		gui.drawRectangle(window, x, y, w, h, "transparent", "#FF0000")

