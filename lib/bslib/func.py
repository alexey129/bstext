# Функции для функционального программирования.

import copy
from collections import namedtuple

from pyrsistent import pmap, pvector

# def mergeNamedtuples(tuple1, tuple2):
# 	"""
# 	Функция для объединения двух namedtuple.
# 	"""
# 	# Создаем новый namedtuple, чтобы содержал все поля из обоих
# 	Merged = namedtuple('Merged', tuple1._fields + tuple2._fields)
# 	# Возвращаем новый экземпляр, объединив значения из входящих(tuple1 и tuple2)
# 	return Merged(*tuple1 + (*tuple2))

def addField(named_tuple, field_name, field_value):
	"""
	Добавляет новое поле в именованый кортеж.
	"""
	# Получаем все имена полей
	fields = named_tuple._fields

	# Проверяем, существует ли уже указанное поле
	if field_name in fields:
		raise ValueError(
			f"Field '{field_name}' already exists in the namedtuple.")

	# Создаем новый namedtuple, включая новое поле
	new_fields = fields + (field_name,)  # Добавляем новое поле

	# Создаем новый namedtuple с новыми именами полей
	NewNamedTuple = namedtuple(type(named_tuple).__name__, new_fields)

	# Возвращаем новый namedtuple, передавая значения всех старых полей +
	# новое поле
	return NewNamedTuple(*(getattr(
		named_tuple, f) for f in fields) + (field_value,))

def removeField(named_tuple, field_name):
	# Получаем все имена полей
	fields = named_tuple._fields

	# Проверяем, существует ли указанное поле
	if field_name not in fields:
		raise ValueError(
			f"Field '{field_name}' does not exist in the namedtuple.")

	# Создаем новый namedtuple, исключая указанное поле
	reduced_named_tuple = namedtuple(
		type(named_tuple).__name__, [f for f in fields if f != field_name])
	
	# Возвращаем новый namedtuple, передавая значения всех полей,
	# кроме удаляемого
	return reduced_named_tuple(*(getattr(
		named_tuple, f) for f in fields if f != field_name))

def getValTup(tpl, key):
	if not isinstance(tpl, tuple):
		raise Exception("Параметр не является кортежем.")
	for i in tpl:
		if i[0] == key:
			return i[1]
	raise Exception(f"Значение {key} не найдено.")

def addValTup(tpl, val):
	return tpl + (val,)

def itemsTuple(my_tuple):
	for key, value in my_tuple:
		yield key, value

def setValTup(tuples, key, new_value):
	# Преобразуем кортеж кортежей в список кортежей для изменения
	tuples_list = list(tuples)
	
	for i, (k, v) in enumerate(tuples_list):
		if k == key:
			# Если ключ найден, создаем новый кортеж с обновленным значением
			tuples_list[i] = (k, new_value)
			break  # Выходим из цикла после обновления
	
	# Преобразуем список обратно в кортеж
	return tuple(tuples_list)