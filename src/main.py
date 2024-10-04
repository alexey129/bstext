import lib.bsgui as gui
import src.textEditor as TEdit
from lib.bslib.log import *

def main():
	app = gui.createApp()
	textEdit = TEdit.createTextEditor("myEditor", 0, 0, app.width, app.height)
	app = app._replace(rootWidget = textEdit)
	app.run(app)