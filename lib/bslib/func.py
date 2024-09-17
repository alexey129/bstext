# Функции для функционального программирования.

from pyrsistent import pvector, pmap

# Массив.
def V(vec = [])
	return pvector(vec)

def setV(vec, index, value):
	return vec.set(index, value)

def getV(vec, index):
	return vec[index]

def pushV(vec, value):
	return vec.append(value)

# Словарь.
def D(dct = {})
	return pmap(dct)

def setD(dct, key, value):
	return dct.set(key, value)

def getD(dct, key):
	return dct[key]