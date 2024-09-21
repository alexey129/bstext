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

def convertCoordFromBufferToScreen(a, b, viewBufferCopy):
	"""
	Переводит координаты выделения из буфера в экранные.
	"""
	x1 = y1 = x2 = y2 = 0

	# Номер символа с которого начинается экранный буфер
	screenStart = viewBufferCopy[0].offsetAbs

	# Номер символа с которым заканчивается экранный буфер
	screenEnd = (viewBufferCopy[len(viewBufferCopy)-1].offsetAbs +
				viewBufferCopy[len(viewBufferCopy)-1].length)

	# Если символ не отображается на экране в данный момент.
	if a < screenStart:
		x1 = 0
		y1 = 0
	if b < screenStart:
		x1 = None
		y1 = None
	if a > screenEnd:
		x2 = None
		y2 = None
	if b > screenEnd:
		x2 = 0
		y2 = 0

	for count, i in enumerate(viewBufferCopy):
		left = i.offsetAbs + i.offsetDop
		right = i.offsetAbs + i.offsetDop + i.length
		if left < a < right:
			x1 = a - (left)
			y1 = count
		if left < b < right:
			x2 = b - (left)
			y2 = count
	return (x1, y1, x2, y2)

def selectionRender(window, sels, vbc, cur, sel):
	# Размеры курсора.
	w = 2
	h = 20

	# Верхний левый угол текстбокса.
	xstart = 20
	ystart = 50

	# Размеры одного символа.
	sw = 13
	sh = 20

	a, b = sel
	coords1 = convertCoordFromBufferToScreen(a, b, vbc)

	for i in getSelectionBoxes(coords1, 50, 10, vbc):
		# Проблема в этом коде:
		x = xstart + sw * i["start"]
		y = ystart + sh * i["count"]
		w = sw * (i["end"] - i["start"])
		h = sh
		# -----------------------
		gui.drawRectangle(window, x, y, w, h, "transparent", "#FF0000")

def deleteTextSelection(textBuffer, selection):
	a, b = selection
	coords1 = convertCoordFromBufferToScreen(a, b, textBuffer.viewBufferCopy)
	x1, y1, x2, y2 = coords1
	textBuffer.deleteText(
		textBuffer.getPosInDocument(x1, y1),
		textBuffer.getPosInDocument(x2, y2))