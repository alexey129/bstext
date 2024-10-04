import wx

from config.viewConfig import viewConfig
from lib.bslib.log import *
from src.event import *


def hex_to_rgb(hex_color):
	"""
	Функция, которая принимает цвет в формате HEX (#10F0A3) и возвращает три
	десятичных числа, соответствующих
	красному, зеленому и синему компонентам цвета.
	"""
	# Удаляем # в начале строки
	hex_color = hex_color.lstrip('#')
	
	# Преобразуем HEX-строку в целые числа
	r = int(hex_color[0:2], 16)
	g = int(hex_color[2:4], 16)
	b = int(hex_color[4:6], 16)
	
	return (r, g, b)

def drawText(canvas, text, x, y, color = None):
	font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
		wx.FONTWEIGHT_NORMAL, faceName="hack")
	canvas.SetFont(font)
	if color is None:
		r, g, b = hex_to_rgb(getValTup(viewConfig, "textBoxFontColor"))
	else:
		r, g, b = hex_to_rgb(color)
	canvas.SetTextForeground(wx.Colour(r, g, b))
	canvas.DrawText(text, x, y)

def setBrush(dc, r, g, b, fill = None):
	if fill == "solid" or fill == None:
		dc.SetBrush(wx.Brush(wx.Colour(r, g, b), wx.SOLID))
	elif fill == "transparent":
		dc.SetBrush(wx.Brush(wx.Colour(r, g, b), wx.TRANSPARENT))

def setPen(dc, r, g, b, fill = None):
	if fill == "solid" or fill == None:
		dc.SetPen(wx.Pen(wx.Colour(r, g, b), 1, wx.SOLID))
	elif fill == "transparent":
		dc.SetPen(wx.Pen(wx.Colour(r, g, b), 1, wx.TRANSPARENT))

def setFillAndBorder(dc, fill, border):
	if fill == None:
		fill = "transparent"
	if border == None:
		border = "transparent"

	if fill == "transparent":
		setBrush(dc, 0, 0, 0, "transparent")
	else:
		r, g, b = hex_to_rgb(fill)
		setBrush(dc, r, g, b)

	if border == "transparent":
		setPen(dc, 0, 0, 0, "transparent")
	else:
		r, g, b = hex_to_rgb(border)
		setPen(dc, r, g, b)

def drawRectangle(canvas, x, y, width, height, fill, border = None):
	setFillAndBorder(canvas, fill, border)
	canvas.DrawRectangle(x, y, width, height)

def drawRoundedRectangle(window, x, y, width, height, round,
									  fill, border):
	canvas = window.canvas
	setFillAndBorder(canvas, fill, border)
	canvas.DrawRoundedRectangle(x, y, width, height, round)

def drawEllipse(window, x, y, width, height, fill, border):
	canvas = window.canvas
	setFillAndBorder(canvas, fill, border)
	canvas.DrawEllipse(x, y, width, height)

def clearWindow(window, canvas):
	canvas.SetPen(wx.TRANSPARENT_PEN)
	canvas.SetBrush(wx.WHITE_BRUSH)
	w, h = window.frame.GetClientSize()
	canvas.DrawRectangle(0, 0, w, h)

Window = namedtuple("Window", (
	"app",
	"frame",
	"width",
	"height",
	"run",
	"rootWidget",
))

# class Window:
# 	def __init__(self, title, width, height):
# 		self.app = wx.App()
# 		self.frame = wx.Frame(parent=None, title=title, size=(width, height))
# 		self.width = width
# 		self.height = height

def setRenderEventHandler(window, func):
	window.frame.Bind(wx.EVT_PAINT, func)

def setCharKeyEventHandler(window, func):
	window.frame.Bind(wx.EVT_CHAR, func)

def setKeyDownEventHandler(window, func):
	window.frame.Bind(wx.EVT_KEY_DOWN, func)

def setKeyUpEventHandler(window, func):
	window.frame.Bind(wx.EVT_KEY_UP, func)

def setMouseWheelEventHandler(window, func):
	window.frame.Bind(wx.EVT_MOUSEWHEEL, func)

def setMouseLeftHandler(window, func):
	window.frame.Bind(wx.EVT_LEFT_DOWN, func)

def setMouseRightHandler(window, func):
	window.frame.Bind(wx.EVT_RIGHT_DOWN, func)

def setMouseMoveHandler(window, func):
	window.frame.Bind(wx.EVT_MOTION, func)

# Рисует окно на экране.
def runWindow(window):
	window.frame.Show(True)
	#wx.GetApp().MainLoop()
	window.app.MainLoop()

def updateWindow(window):
	window.frame.Refresh()
	window.frame.Update()

def createApp():
	app = wx.App()
	width, height = wx.GetDisplaySize()
	newApp = Window(
		app = app,
		frame = wx.Frame(parent=None, title="BSText", size=(width//2, height//2)),
		width = width,
		height = height,
		run = runFunc,
		rootWidget = None,
	)
	return newApp

# Отдельно дерево виджетов-объектов и отдельно функция которая принимает
# любой виджет(он уже полностью готовый и измененный как надо), рисует белый
# прямоугольник и вызывает у него и у всех его детей из массива children
# функцию для перерисовки.
def runFunc(window):
	rootWidget = window.rootWidget
	# Разворачиваем окно на весь экран.
	#window.frame.Maximize()

	def keyPressHandler(key):
		nonlocal rootWidget
		nonlocal window
		rootWidget = rootWidget.onKeyPress(rootWidget, key)
		updateWindow(window)

	def renderEventHandler(event1):
		nonlocal rootWidget
		nonlocal window
		# window.canvas = wx.PaintDC(window.frame)
		canvas = wx.PaintDC(window.frame)
		clearWindow(window, canvas)
		rootWidget.onPaint(rootWidget, canvas)

	def symbolPressHandler(event1):
		symbol = chr(event1.GetUnicodeKey())
		if symbol != None:
			keyPressHandler(symbol)
		else:
			# Обработка других нажатий клавиш
			event1.Skip()

	def nonCharPressHandler(event1):
		keyCode = event1.GetKeyCode()
		if keyCode == wx.WXK_UP:
			keyPressHandler("up")
		elif keyCode == wx.WXK_DOWN:
			keyPressHandler("down")
		elif keyCode == wx.WXK_LEFT:
			keyPressHandler("left")
		elif keyCode == wx.WXK_RIGHT:
			keyPressHandler("right")
		elif keyCode == wx.WXK_BACK:
			keyPressHandler("backspace")
		elif keyCode == wx.WXK_SHIFT:
			keyPressHandler("shift")
		else:
			# Обработка других нажатий клавиш
			event1.Skip()

	def mouseWheelEventHandler(event1):
		rotation = event1.GetWheelRotation()
	
		if rotation > 0:
			keyPressHandler("mouseWheelUp")
		else:
			keyPressHandler("mouseWheelDown")

	def keyRealizeHandler(event1):
		keyCode = event1.GetKeyCode()
		if keyCode == wx.WXK_SHIFT:
			keyPressHandler("shiftRealize")
		else:
			# Обработка других нажатий клавиш
			event1.Skip()

	def mouseButtonHandler(event):
		# Получаем координаты курсора
		x, y = event.GetPosition()
		
		# Обработка события
		if event.LeftIsDown():
			keyPressHandler("mouseLeft_"+str(x)+"_"+str(y))
		elif event.RightIsDown():
			keyPressHandler("mouseRight_"+str(x)+"_"+str(y))
		# elif event.Moving():
			# keyPressHandler("mouseMove_"+str(x)+"_"+str(y))

	setRenderEventHandler(window, renderEventHandler)

	setCharKeyEventHandler(window, symbolPressHandler)

	setKeyDownEventHandler(window, nonCharPressHandler)

	setMouseWheelEventHandler(window, mouseWheelEventHandler)

	setKeyUpEventHandler(window, keyRealizeHandler)

	setMouseLeftHandler(window, mouseButtonHandler)

	setMouseRightHandler(window, mouseButtonHandler)

	setMouseMoveHandler(window, mouseButtonHandler)

	runWindow(window)
