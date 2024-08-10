from src.textBox import *
from var_dump import var_dump

from src.textBuffer import *
from src.selection import *

def updateSelectionCoordTest():
	tb = TextBuffer()
	sl = Selection1(tb)
	var_dump(updateSelectionCoord(sl, tb))

def start():
	updateSelectionCoordTest()