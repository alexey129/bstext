def startSymSlice(str, symbol):
	"""
	Обрезает строку от начала и до первого вхождения определенного символа.
	Сам символ входит в итоговую строку.
	"""
	str = str[str.find(symbol):]
	return str

def startSymSliceWithout(str, symbol):
	"""
	Обрезает строку от начала и до первого вхождения определенного символа.
	Сам символ не входит в итоговую строку.
	"""
	str = str[str.find(symbol) + 1:]
	return str

def endSymSlice(str, symbol):
	"""
	Обрезает строку от конца и до первого вхождения определенного символа.
	Сам символ входит в итоговую строку.
	"""
	str = str[:str.rfind(symbol)+1]
	return str

def endSymSliceWithout(str, symbol):
	"""
	Обрезает строку от конца и до первого вхождения определенного символа.
	Сам символ не входит в итоговую строку.
	"""
	str = str[:str.rfind(symbol)]
	return str

def findCorrespBracket(str, index):
	"""
	Ищет соответсвующую скобку в строке. Принимает строку и номер символа в
	строке где находится скобка. Возвращает номер символа соответствующей
	скобки.
	"""
	openBracket = ""
	closeBracket = ""
	if str[index] == "(":
		openBracket = "("
		closeBracket = ")"
	elif str[index] == "{":
		openBracket = "{"
		closeBracket = "}"
	elif str[index] == "[":
		openBracket = "["
		closeBracket = "]"
	countBracket = 0
	while index < len(str):
		if(str[index]) == openBracket:
			countBracket += 1
		elif (str[index]) == closeBracket:
			countBracket -= 1
		if countBracket == 0:
			return index
		index += 1
	return None

def getBracketText(string, index):
	"""
	Ищет соответсвующую скобку в строке и возвращает текст внутри скобок.
	"""
	if string[index] in ("(", "[", "{", ):
		i = findCorrespBracket(string, index)
		return string[index+1:i]
	else:
		return Error("Входное значение не является скобкой")

def clearStrSpace(str, space = True, tab = True, newLine = True,):
	"""
	Убирает в строке символы переноса, табы и заменяет несколько пробелов н
	один.
	"""
	i = 0
	while i < len(str):
		# Если надо убирать пробелы.
		if i > 0 and (str[i] == " " and str[i-1] == " ") and space:
			str = str[:i] + str[i+1:]
		# Если надо убирать переносы строки.
		elif str[i] == "\n" and newLine:
			str = deleteStr(str, i, i+1)
		# Если надо убирать табы.
		elif str[i] == "\t" and tab:
			str = deleteStr(str, i, i+1)
		else:
			i += 1
	return str

def insertStr(str1, str2, index):
	"""
	Вставляет строку str2 в строку str1 на позицию index.
	"""
	return str1[:index] + str2 + str1[index:]

def deleteStr(str, start, end):
	"""
	Удаляет символы в строке от start до end.
	"""
	return str[:start] + str[end:]


def findStr(string1, string2):
	res = string1.find(string2)
	if res != -1:
		return res
	else:
		return Error("Подстрока не найдена")