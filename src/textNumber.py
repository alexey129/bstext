import lib.bsgui as gui
from config.viewConfig import viewConfig

def render(window, props, parentProps):
	#gui.drawText(window, "My TextArea", 20, 20)
	#gui.drawRectangle(window, 20, 20, 800, 300, "transparent", "#FF0000")
	count = 50
	num = None
	for i in props["text"]:
		if num != i.absNum:
			gui.drawText(window, str(i.absNum), 5, count,
				viewConfig["textBoxLineNumberColor"])
			num = i.absNum
		count += 20