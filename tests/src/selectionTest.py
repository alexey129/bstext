from src.selection import *
from var_dump import var_dump

def setDataCoordTest():
	coord = pmap({"x1": 0, "y1": 0, "x2": 0, "y2": 0})
	coord = setDataCoord(coord, 15, 10, 2, 4)
	if not (coord == {"x1": 15, "y1": 10, "x2": 2, "y2": 4}):
		raise Exception("Тест не пройден")

def expandDataCoordTest():
	coord = pmap({"x1": 1, "y1": 1, "x2": 2, "y2": 2})
	coord = expandDataCoord(coord, 3, 3)
	if not (coord == {"x1": 1, "y1": 1, "x2": 3, "y2": 3}):
		raise Exception("Тест не пройден")
	coord = expandDataCoord(coord, 0, 0)
	if not (coord == {"x1": 0, "y1": 0, "x2": 3, "y2": 3}):
		raise Exception("Тест не пройден")

def getSelectBoxesTest():
	var_dump(getSelectBoxes(pmap({"x1": 2, "y1": 1, "x2": 5, "y2": 5}),10))

def start():
	setDataCoordTest()
	expandDataCoordTest()
	getSelectBoxesTest()