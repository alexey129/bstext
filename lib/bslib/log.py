from collections import namedtuple
import lib.bslib.string as strlib

def isNamedtuple(instance):
    return isinstance(instance, tuple) and hasattr(instance, '_fields')

def isTuple(instance):
    return isinstance(instance, tuple) and not(hasattr(instance, '_fields'))

def serializeNamedtuple(arg):
	a = "{"
	count = 0
	for key, value in arg._asdict().items():
		count += 1
		if count < len(arg):
			a += str(key) + ": " + sublog(value) + ","
		else:
			a += str(key) + ": " + sublog(value)
	return a + "}"

def serializeTuple(arg):
	a = "("
	count = 0
	for i in arg:
		count += 1
		if count < len(arg):
			a += sublog(i) + ","
		else:
			a += sublog(i)
	return a + ")"

def serializeCommon(arg):
	return str(arg)

def sublog(arg):
	string = ""
	if isTuple(arg):
		string += serializeTuple(arg)
	elif isNamedtuple(arg):
		string += serializeNamedtuple(arg)
	else:
		string += serializeCommon(arg)
	return string

def log(*args):
	"""
	Выводит на экран с отступами в форматированном виде обычные переменные,
	кортежи и именованные кортежи. Параметры можно передавать просто через
	запятую.
	"""
	for arg in args:
		bbb = sublog(arg)
		indent = 0

		indentStr = " "
		indentLen = len(indentStr)

		i = 0
		while i < len(bbb):
			if bbb[i] in (","):
				bbb = strlib.insertStr(bbb, "\n"+indentStr*indent, i + 1)
				i = i + indentLen + indent
			elif bbb[i] in ("(", "{"):
				indent += 1
				bbb = strlib.insertStr(bbb, "\n"+indentStr*indent, i + 1)
				i = i + indentLen + indent
			elif bbb[i] in (")", "}"):
				indent -= 1
				bbb = strlib.insertStr(bbb, "\n"+indentStr*indent, i)
				i = i + indentLen + 1 + indent
			else:
				i = i + 1
		print(bbb)
