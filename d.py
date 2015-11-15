__author__ = 'sam <vogelsangersamuel@hotmail.com>'

import numpy as np


# noinspection PyPep8Naming
class d(object):
	def __init__(self, *args, **kwargs):
		if len(args) == 1:
			faces = args[0]
			self.values = np.arange(faces) + 1
			self.expectancies = np.ones(faces)
			self.normalizeExpectancies()
			self.length = faces
		elif len(args) == 3:
			self.values = args[0]
			self.expectancies = args[1]
			self.length = args[2]
		elif all(x in kwargs.keys() for x in ['values', 'length']):
			self.values = kwargs.get("values")
			self.expectancies = np.array([])
			self.length = kwargs.get("length")

	def __add__(self, other):
		if isinstance(other, d):
			return self.addDice(other)
		elif isinstance(other, (int, float)):
			return d(self.values + other, self.expectancies, self.length)

	def __radd__(self, other):
		return self+other

	def __mul__(self, other):
		if isinstance(other, int):
			return self.times(other)

	def __rmul__(self, other):
		return self*other

	def __lt__(self, other):
		return

	def __str__(self):
		return str(self.values)

	def addDice(self, other):
		newLength = self.length + other.length - 1
		newValues = np.arange(self.values[0]+other.values[0], self.values[-1] + other.values[-1] + 1)
		newExpectancies = np.zeros((newLength, ))
		for i in np.arange(self.length):
			newExpectancies[i:i+other.length] += (self.expectancies[i] * other.expectancies)
		newExpectancies = d.normalize(newExpectancies)
		return d(newValues, newExpectancies, newLength)

	def times(self, factor):
		if factor == 0:
			return d(0)
		elif factor == 1:
			return self
		else:
			return self + self.times(factor-1)

	def meanValueWeighted(self):
		return np.average(self.values, weights=self.expectancies)

	def normalizedExpectancies(self):
		return self.expectancies / np.sum(self.expectancies)

	def normalizeExpectancies(self):
		self.expectancies /= np.sum(self.expectancies)

	@staticmethod
	def normalize(expectancies):
		return expectancies / np.sum(expectancies)
