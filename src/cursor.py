from src.event import *
import lib.bsgui as gui

class Cursor:
	"""
	Это только представление курсора и отвечает только за рисование его на
	экране.
	"""
	def __init__(self, window):
		self.className = "Cursor"
		self.name = "bsText"
		self.eventDispatcher = EventDispatcher()
		self.eventDispatcher.setHandler("keyPress", self.keyPressHandler)
		self.children = {}

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

		curs = props["cursor"]
		# Верхний левый угол курсора.
		xc = xstart + curs.x*sw
		yc = ystart + curs.y*sh
		gui.drawRectangle(window, xc, yc, w, h, "transparent", "#FF0000")