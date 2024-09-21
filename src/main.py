import wx

from src.textBuffer import *
import src.textEditor as TEdit
import src.event as event
import lib.bsgui as gui
from lib.bslib.func import *
from lib.bslib.log import *

# Отдельно дерево виджетов-объектов и отдельно функция которая принимает
# любой виджет(он уже полностью готовый и измененный как надо), рисует белый
# прямоугольник и вызывает у него и у всех его детей из массива children
# функцию для перерисовки.
def main():
	window = gui.Window("BSText", 1200, 600)
	textEditor = TEdit.createTextEditor(window, "myEditor", 0, 0, 1000, 500)

	def keyPressHandler(key):
		nonlocal textEditor
		nonlocal window
		textEditor = textEditor.onKeyPress(textEditor, key)
		gui.updateWindow(window)

	def renderEventHandler(event1):
		nonlocal textEditor
		nonlocal window
		window.canvas = wx.PaintDC(window.frame)
		gui.clearWindow(window)
		TEdit.render(textEditor)

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

	gui.setRenderEventHandler(window, renderEventHandler)

	gui.setCharKeyEventHandler(window, symbolPressHandler)

	gui.setKeyDownEventHandler(window, nonCharPressHandler)

	gui.setMouseWheelEventHandler(window, mouseWheelEventHandler)

	gui.setKeyUpEventHandler(window, keyRealizeHandler)

	gui.runWindow(window)
