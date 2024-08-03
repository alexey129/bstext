import wx

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

def drawText(window, text, x, y):
	font = wx.Font(16, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
		wx.FONTWEIGHT_NORMAL, faceName="courier new")
	window.canvas.SetFont(font)
	window.canvas.DrawText(text, x, y)

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

def drawRectangle(window, x, y, width, height, fill, border):
	canvas = window.canvas
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

def clearWindow(window):
	window.canvas.SetPen(wx.TRANSPARENT_PEN)
	window.canvas.SetBrush(wx.WHITE_BRUSH)
	w, h = window.frame.GetClientSize()
	window.canvas.DrawRectangle(0, 0, w, h)

def createdWindow():
	print("window is created")

class Window:
	def __init__(self, title, width, height):
		self.app = wx.App()
		self.frame = wx.Frame(parent=None, title=title, size=(width, height))
		self.canvas = None
		self.width = width
		self.height = height
		self.eventDispatcher = EventDispatcher()
		self.eventDispatcher.setHandler("createWindow", createdWindow)
		self.eventDispatcher.emit("createWindow")

	def updateWindow(self):
		self.frame.Refresh()
		self.frame.Update()

def setRenderEventHandler(window, func):
	window.frame.Bind(wx.EVT_PAINT, func)

def setCharKeyEventHandler(window, func):
	window.frame.Bind(wx.EVT_CHAR, func)

def setKeyDownEventHandler(window, func):
	window.frame.Bind(wx.EVT_KEY_DOWN, func)

def setMouseWheelEventHandler(window, func):
	window.frame.Bind(wx.EVT_MOUSEWHEEL, func)

# Рисует окно на экране.
def runWindow(window):
	window.frame.Show(True)
	#wx.GetApp().MainLoop()
	window.app.MainLoop()

def updateWindow(window):
	window.frame.Refresh()
	window.frame.Update()