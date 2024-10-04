from var_dump import var_dump

from src.selection import *
from src.textBox import *
from src.textBuffer import *


def updateSelectionCoordTest():
	tb = TextBuffer()
	sl = Selection1(tb)
	var_dump(updateSelectionCoord(sl, tb))

def start():
	updateSelectionCoordTest()