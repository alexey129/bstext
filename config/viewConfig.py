# Тут находятся настройки внешнего вида редактора.

from pyrsistent import pvector, pmap

viewConfig = pmap({
	# Цвет фона у текстбокса.
	"textBoxBackgroundColor": "#24292E",
	# Цвет текст в текстбоксе.
	"textBoxFontColor": "#FAFBFC",
	# Ширина текста на экране в символах.
	"textBoxTextWidth": 80,
	# Размер шрифта в текстбоксе
	"textBoxFontSize": 16,
	# Цвет фона выделения.
	"textBoxSelectionBackgroudColor": "#111111",
	# Цвет рамки выделения.
	"textBoxSelectionBorderColor": "#666666",
	# Цвет цифр у номеров строк.
	"textBoxLineNumberColor": "#222222",
})