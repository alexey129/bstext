import wx

from src.textBuffer import *
from src.textEditor import *
from src.event import *
import lib.bsgui as gui

# Сплошной набор символов.





# Отдельно дерево виджетов-объектов и отдельно функция которая принимает
# любой виджет(он уже полностью готовый и измененный как надо), рисует белый
# прямоугольник и вызывает у него и у всех его детей из массива children
# функцию для перерисовки.
def main():
	window = gui.Window("BSText", 1200, 600)
	textEditor = TextEditor(window)
	def keyPressHandler(params):
		textEditor.eventDispatcher.emit("keyPress", params)

	eventDispatcher = EventDispatcher()
	eventDispatcher.setHandler("keyPress", keyPressHandler)

	def aaa1(event):
		window.canvas = wx.PaintDC(window.frame)
		gui.clearWindow(window)
		textEditor.render(window, {
			"x": 0,
			"y": 0,
			"width": 1000,
			"height": 500,
		}, {})

	def aaa2(event):
		symbol = chr(event.GetUnicodeKey())
		if symbol != None:
			eventDispatcher.emit("keyPress", {"key": symbol})
		else:
			# Обработка других нажатий клавиш
			event.Skip()

	def aaa3(event):
		keyCode = event.GetKeyCode()
		if keyCode == wx.WXK_UP:
			eventDispatcher.emit("keyPress", {
				"key":"up",
			})
		elif keyCode == wx.WXK_DOWN:
			eventDispatcher.emit("keyPress", {
				"key":"down",
			})
		elif keyCode == wx.WXK_LEFT:
			eventDispatcher.emit("keyPress", {
				"key":"left",
			})
		elif keyCode == wx.WXK_RIGHT:
			eventDispatcher.emit("keyPress", {
				"key":"right",
			})
		elif keyCode == wx.WXK_BACK:
			eventDispatcher.emit("keyPress", {
				"key":"backspace",
			})
		else:
			# Обработка других нажатий клавиш
			event.Skip()

	def aaa4(event):
		rotation = event.GetWheelRotation()
	
		if rotation > 0:
			eventDispatcher.emit("keyPress", {
				"key":"mouseWheelUp",
			})
		else:
			eventDispatcher.emit("keyPress", {
				"key":"mouseWheelDown",
			})

	gui.setRenderEventHandler(window, aaa1)

	gui.setCharKeyEventHandler(window, aaa2)

	gui.setKeyDownEventHandler(window, aaa3)

	gui.setMouseWheelEventHandler(window, aaa4)

	gui.runWindow(window)
