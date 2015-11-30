__author__ = 'sam <vogelsangersamuel@hotmail.com>, piMoll'

import numpy as np
import matplotlib.pyplot as plt


# noinspection PyPep8Naming
class d(object):
	def __init__(self, *args, **kwargs):
		if len(args) == 1:
			faces = args[0]
			self.data = np.array([np.arange(faces) + 1, np.ones(faces)])
			self.normalizeExpectancies()
			self.length = faces
		elif len(args) == 2:
			self.data = args[0]
			self.length = args[1]
		elif len(args) == 3:
			self.data = np.vstack((args[0], args[1]))
			self.length = args[2]
		elif all(x in kwargs.keys() for x in ['values', 'length']):
			self.data = np.vstack((kwargs.get("values"), kwargs.get("length")))
			self.length = kwargs.get("length")

	def __add__(self, other):
		if isinstance(other, d):
			return self.__addDice(other)
		elif isinstance(other, (int, float)):
			return d(self.data[0] + other, self.data[1], self.length)

	def __radd__(self, other):
		return self + other

	def __mul__(self, other):
		if isinstance(other, int):
			return self.times(other)

	def __rmul__(self, other):
		return self * other

	def __iter__(self):
		return iter(np.swapaxes(self.data, 0, 1))

	def __lt__(self, other):
		if isinstance(other, (int, float)):
			return np.where(self.data[0] > other, True, False)
		else:
			raise TypeError

	def __gt__(self, other):
		return

	def __le__(self, other):
		return

	def __ge__(self, other):
		return

	def __str__(self):
		return "dice: " + str(self.data[0])

	def __addDice(self, other):
		newLength = self.length + other.length - 1
		newValues = np.arange(self.data[0, 0] + other.data[0, 0], self.data[0, -1] + other.data[0, -1] + 1)

		newExpectancies = np.zeros((newLength,))
		for i in np.arange(self.length):
			newExpectancies[i:i + other.length] += (self.data[1, i] * other.data[1])
		newExpectancies = d.normalize(newExpectancies)

		return d(newValues, newExpectancies, newLength)

	def times(self, factor):
		if factor == 0:
			return d(0)
		elif factor == 1:
			return self
		else:
			return self.__addDice(self.times(factor - 1))

	@DeprecationWarning  # Currently not used
	def meanValueWeighted(self):
		return np.average(self.data[0], weights=self.data[1])

	def meanValueAndExpectancy(self):
		index = self.meanIndex()
		index_int = np.floor(index)

		values = self.data[0]
		valueBounds = values[index_int:index_int + 2]
		value = valueBounds[0] + (index % 1) * (valueBounds[1] - valueBounds[0])

		expectancies = self.data[1]
		expectancyBounds = expectancies[index_int:index_int + 2]
		expectancy = expectancyBounds[0] + (index % 1) * (expectancyBounds[1] - expectancyBounds[0])

		return value, expectancy

	def meanIndex(self):
		return np.average(np.arange(self.length), weights=self.data[1])

	def normalizeExpectancies(self):
		self.data[1] = d.normalize(self.data[1])

	@staticmethod
	def normalize(expectancies):
		return expectancies / np.sum(expectancies)

	def plot(self):
		plot(self)

	def values(self):
		return self.data[0]

	def expectancies(self):
		return self.data[1]


def plot(dice):
	xdata = dice.values()
	ydata = dice.expectancies() * 100

	meanVal, meanExp = dice.meanValueAndExpectancy()

	plt.plot(meanVal, meanExp * 100, 'ro')

	plt.plot(xdata, ydata)

	plt.xlabel('dice rolls')
	plt.ylabel('likelihood (in percent)')
	plt.title('DnDice')
	plt.grid(True)

	# plt.savefig("test.png")
	plt.show()
