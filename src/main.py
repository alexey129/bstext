import wx

from src.textBuffer import *
import src.textEditor as TEdit
import src.event as event
import lib.bsgui as gui
from lib.bslib.func import *
from lib.bslib.log import *

def main():
	app = gui.createApp()
	textEdit = TEdit.createTextEditor("myEditor", 0, 0, 1000, 500)
	app = app._replace(rootWidget = textEdit)
	app.run(app)

