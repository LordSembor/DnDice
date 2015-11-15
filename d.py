__author__ = 'sam <vogelsangersamuel@hotmail.com>'

import numpy as np


# noinspection PyPep8Naming
class d(object):
	def __init__(self, *args, **kwargs):
		if len(args) == 1:
			faces = args[0]
			self.values = np.arange(faces) + 1
			self.expectancies = np.ones(faces)
			self.length = faces
		elif all(x in kwargs.keys() for x in ['values', 'length']):
			self.values = kwargs.get("values")
			self.expectancies = np.array([])
			self.length = kwargs.get("length")
		elif len(args) == 2:
			self.values = args[0]
			self.expectancies = np.array([])
			self.length = args[1]

	def __add__(self, other):
		if isinstance(other, d):
			return self.addDice(other)
		elif isinstance(other, (int, float)):
			return d(values=self.values + other, length=self.length)

	def __radd__(self, other):
		return self+other

	def __mul__(self, other):
		if isinstance(other, int):
			return self.times(other)

	def __rmul__(self, other):
		return self*other

	def __str__(self):
		return str(self.values)

	def addDice(self, other):
		ones = np.ones((1, other.length))
		first = self.values.reshape(self.length, 1)
		values = (np.dot(first, ones) + other.values).flatten()
		return d(values=values, length=values.size)

	def times(self, factor):
		if factor == 0:
			return d(0)
		elif factor == 1:
			return self
		else:
			return self + self.times(factor-1)



