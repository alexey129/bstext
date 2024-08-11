import copy
from var_dump import var_dump

import lib.bslib.string as strlib

class Selection:
	def __init__(self):
		self.start = 0
		self.end = 0

class ViewLine:
	"""
	Подстрока в тексте, если строка переносится на другую строку.
	"""
	def __init__(self, text = "", n1 = 0, n2 = 0, n3 = 0, n4 = 0, n5 = 0):
		self.text = text
		self.absNum = n1 # Номер строки относительно всего документа.
		# Смещение строки относительно начала документа.
		self.offsetAbs = n2
		self.dopNum = n3 # Номер подстроки если строка разделилась при
						   # переносе.
		# Смещение подстроки относительно строки.
		self.offsetDop = n4
		# Длина подстроки.
		self.length = n5

class Cursor:
	def __init__(self):
		# Координаты считаем в символах.
		self.x = 0
		self.y = 0
		self.lenghtLine = 30

	def up(self, buf):
		if self.y == 0:
			pass
		elif self.y > 0:
			self.y -= 1
			if self.x > buf.viewBufferCopy[buf.cursor.y].length:
				self.x = buf.viewBufferCopy[buf.cursor.y].length

	def down(self, buf):
		if self.y == buf.lineCountScreen - 1:
			pass
		else:
			self.y += 1
			if self.x > buf.viewBufferCopy[buf.cursor.y].length:
				self.x = buf.viewBufferCopy[buf.cursor.y].length

	def left(self, buf):
		self.x -= 1
		if self.x < 0 and self.y == 0:
			self.x = 0
		elif self.x < 0 and self.y > 0:
			self.x = buf.viewBufferCopy[buf.cursor.y - 1].length
			self.y -= 1

	def right(self, buf, perenos):
		# perenos - надо ли при переходе вправо оставаться в конце строки или
		# сразу переходить на новую строку(нужно для печати символов).
		if perenos:
			if self.x + 1 < buf.viewBufferCopy[buf.cursor.y].length:
				self.x += 1
			else:
				self.x = 0
				self.down(buf)
		else:
			if self.x + 1 < buf.viewBufferCopy[buf.cursor.y].length + 1:
				self.x += 1
			else:
				self.x = 0
				self.down(buf)

class TextBuffer:
	def __init__(self):
		self.buf = ""
		self.newLineArray = []
		# Массив из ViewLine, в котором хранится тот же самый текст что сейчас
		# находится на экране.
		self.viewBufferCopy = []
		self.lineWidth = 50 # Максимальная длина строки на экране.
		self.currenUpLineCount = 0 # Номер подстроки считая от начала текста,
		                           # которая находится на экране на самом верху.
		self.lineCountScreen = 10 # Максимальное кол-во строк на экране.
		self.cursor = Cursor()
		self.cursor.lenghtLine = self.lineWidth

		self.allCountDopLine = 0 # Общее кол-во подстрок на экране.

		self.selection = None

	def setText(self, text):
		self.buf = text

	def getText(self):
		return self.buf

	def addNewLine(self, num):
		self.newLineArray.append(num)

	def deleteNewLine(self, num):
		self.newLineArray.remove(num)

	def setTextFromFile(self, path):
		with open(path, "r", encoding="utf-8") as file:
			self.buf = file.read()

		# Разбираем текст на строки.
		self.newLineArray.append(0)
		count = 0
		while count < len(self.buf):
			i = self.buf[count]
			if i == "\n":
				self.newLineArray.append(count)
				self.buf = strlib.deleteStr(self.buf, count, count+1)
			else:
				count += 1
		#print(self.newLineArray)
		#print(strlib.deleteStr("abcdefghijk", 0, 2))

	def getViewText(self):
		# Разбиваем текст на строки.
		strings = []
		i = 0
		while i < len(self.newLineArray) - 1:
			# Берем промежуток от одного переноса строки до другого.
			strings.append(self.buf[self.newLineArray[i]:self.newLineArray[i+1]])
			i += 1
		
		# Разбиваем строки на подстроки.
		newStrings = []
		for i in strings:
			dops = []
			while len(i) > 0:
				if len(i) > self.lineWidth:
					dops.append(i[:self.lineWidth])
					i = i[self.lineWidth:]
				else:
					dops.append(i)
					break
			newStrings.append(dops)
		#print(newStrings)

		# Составляем массив из полностью готовых строк.
		viewLines = []
		offset = 0
		for i in range(len(newStrings)):
			for j in range(len(newStrings[i])):
				viewLines.append(ViewLine(
					newStrings[i][j],
					i,
					self.newLineArray[i],
					j,
					offset,
					len(newStrings[i][j])
				))
				offset += len(newStrings[i][j])
			offset = 0

		#self.viewBufferCopy = viewLines
		self.allCountDopLine = len(viewLines)
		self.viewBufferCopy = viewLines[self.currenUpLineCount:
			self.currenUpLineCount + self.lineCountScreen]

		return self.viewBufferCopy

	def addSymbol(self, symbol):
		"""
		Добавляет новый символ.
		"""
		currentStr = self.viewBufferCopy[self.cursor.y]
		# Номер строки относительно документа, на которой находится этот символ.
		lineNum = currentStr.absNum
		# Позиция в этой строке куда надо вставить символ.
		linePosNum = self.cursor.x + currentStr.offsetDop
		# Позиция относительно начала документа
		res = currentStr.offsetAbs + linePosNum

		self.buf = strlib.insertStr(self.buf, symbol,
			res)

		# TODO: Надо изменить массив newLineArray.

		for count, item in enumerate(self.newLineArray):
			if item > currentStr.offsetAbs:
				self.newLineArray[count] += 1



	def delSymbol(self):
		"""
		Удаляет символ перед курсором(не тот на который указывает курсор, а
		перед ним).
		"""
		# Получаем текущую подстроку.
		currentStr = self.viewBufferCopy[self.cursor.y]
		# Номер строки относительно документа, на которой находится этот символ.
		lineNum = currentStr.absNum
		# Позиция в этой строке куда надо вставить символ.
		linePosNum = self.cursor.x + currentStr.offsetDop
		if linePosNum > 0:
			#linePosNum -= 1
			self.buf = strlib.deleteStr(self.buf,
				currentStr.offsetAbs + linePosNum - 1,
				currentStr.offsetAbs + linePosNum )
			# TODO: Надо изменить массив newLineArray.
		for count, item in enumerate(self.newLineArray):
			if item > currentStr.offsetAbs:
				self.newLineArray[count] -= 1

	def getCursorPosInDocument(self):
		"""
		Возвращает позицию текущего символа на который указывает курсор в
		документе.
		"""
		currentStr = self.viewBufferCopy[self.cursor.y]
		# Номер строки относительно документа, на которой находится этот символ.
		lineNum = currentStr.absNum
		# Позиция в этой строке куда надо вставить символ.
		linePosNum = self.cursor.x + currentStr.offsetDop
		# Позиция относительно начала документа
		res = currentStr.offsetAbs + linePosNum
		return res

	def getPosInDocument(self, x, y):
		"""
		Возвращает позицию текущего символа на который указывает координата x,y.
		"""
		currentStr = self.viewBufferCopy[y]
		# Номер строки относительно документа, на которой находится этот символ.
		lineNum = currentStr.absNum
		# Позиция в этой строке куда надо вставить символ.
		linePosNum = x + currentStr.offsetDop
		# Позиция относительно начала документа
		res = currentStr.offsetAbs + linePosNum
		return res

	def scrollUp(self):
		if self.currenUpLineCount > 0:
			self.currenUpLineCount -= 1

	def scrollDown(self):
		if self.currenUpLineCount < self.allCountDopLine - self.lineCountScreen:
			self.currenUpLineCount += 1

	def addSelectionLeft(self):
		pass

	def addSelectionRight(self):
		if self.selection == None:
			self.selection = Selection()
			self.selection.start = self.selection.end = self.getCursorPosInDocument()
		self.selection.end += 1

	def deleteText(self, a, b):
		self.buf = strlib.deleteStr(self.buf, a, b)

		for count, item in enumerate(self.newLineArray):
			if a < item < b:
				self.newLineArray.pop(count)

		currentStr = self.viewBufferCopy[self.cursor.y]
		for count, item in enumerate(self.newLineArray):
			if item > currentStr.offsetAbs:
				self.newLineArray[count] -= (b - a)