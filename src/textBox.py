from src.event import *
from src.textArea import *
from src.selection import *
import lib.bsgui as gui
from var_dump import var_dump

def expandDataCoord(selectionRangeCoord, cursorCoord):
	"""
	Расширяет выделение до какого то символа. Возвращает новое выделение.
	TODO: Надо сделать чтоб не только расширяло но и сжимало.
	"""
	sx1, sy1, sx2, sy2 = selectionRangeCoord
	cx, cy = cursorCoord
	if ((cx < sx1 and cy == sy1) or cy < sy1):
		return (cx, cy, sx2, sy2)
	elif ((cx > sx2 and cy == sy2) or cy > sy2):
		return (sx1, sy1, cx, cy)
	else:
		return (sx1, sy1, sx2, sy2)

def setSelectionRange(selectionRangeCoord, cursor):
	"""
	Принимает текущее выделение и текущую координату курсора, и возвращает
	новые координа выделения.
	"""
	if selectionRangeCoord is None:
		# -1 тут нужен чтоб создавать выделение сразу когда впервые сдвинулись
		# вправо.
		return (cursor.x - 1, cursor.y, cursor.x, cursor.y)
	else:
		return expandDataCoord(selectionRangeCoord, (cursor.x, cursor.y))


class TextBox:
	def __init__(self, window, textBuffer):
		self.window = window
		self.className = "TextBox"
		self.name = "bsText"
		self.eventDispatcher = EventDispatcher()
		self.eventDispatcher.setHandler("keyPress", self.keyPressHandler)
		self.children = {"textArea": TextArea(window)}
		self.text = {} # Массив со строками которые остается просто нарисовать
					   # на экране
		self.textBuffer = textBuffer
		self.isShiftPressed = False

		self.selection = None

	def keyPressHandler(self, params):
		cursor = self.textBuffer.cursor
		self.children["textArea"].eventDispatcher.emit("keyPress")
		if params["key"] == "up":
			cursor.up(self.textBuffer)

		elif params["key"] == "down":
			self.selection = keyDown(self.selection, self.isShiftPressed,
				self.textBuffer)

		elif params["key"] == "left":
			self.textBuffer.cursor.left(self.textBuffer)
			if self.isShiftPressed:
				self.textBuffer.addSelectionLeft()
				self.selection = setSelectionRange(
					self.selection,
					self.textBuffer.cursor)

		elif params["key"] == "right":
			self.textBuffer.cursor.right(self.textBuffer, True)
			if self.isShiftPressed:
				self.textBuffer.addSelectionRight()
				self.selection = setSelectionRange(
					self.selection,
					self.textBuffer.cursor)

		elif params["key"] == "backspace":
			if (not(cursor.x == 0 and
				cursor.y == 0)):
					self.textBuffer.delSymbol()
					cursor.left(self.textBuffer)

		elif params["key"] == "mouseWheelUp":
			self.textBuffer.scrollUp()

		elif params["key"] == "mouseWheelDown":
			self.textBuffer.scrollDown()

		elif params["key"] == "shift":
			self.isShiftPressed = True

		elif params["key"] == "shiftRealize":
			self.isShiftPressed = False

		elif len(params["key"]) == 1:
			self.textBuffer.addSymbol(params["key"])
			cursor.right(self.textBuffer, False)

		self.window.updateWindow()

	def render(self, window, props, parentProps):
		self.text = props[4]
		gui.drawText(window, "My TextBox", 20, 20)
		gui.drawRectangle(window, 20, 20, 800, 300, "transparent", "#FF0000")
		self.children["textArea"].render(window, {
			"text": props[4],
			"cursor": self.textBuffer.cursor,
		}, props)
		if self.selection is not None:
			selectionRender(window,
				{"coords": self.selection}, props)
		# Scrollbar.render(window, self.widget["children"]["scrollbar"],
		# 	{}, props)
