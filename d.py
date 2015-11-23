__author__ = 'sam <vogelsangersamuel@hotmail.com>, piMoll'

import numpy as np
import matplotlib.pyplot as plt


# noinspection PyPep8Naming
class d(object):
	def __init__(self, *args, **kwargs):
		if len(args) == 1:
			faces = args[0]
			self.values = np.arange(faces) + 1
			self.expectancies = np.ones(faces)
			self.normalizeExpectancies()
			self.length = faces
		elif len(args) == 2:
			self.data = args[0]
			self.length = args[1]
			self.values = self.data[0]
			self.expectancies = self.data[1]
		elif len(args) == 3:
			self.data = np.hstack((args[0], args[1]))
			self.length = args[2]
			self.values = self.data[0]
			self.expectancies = self.data[1]
		elif all(x in kwargs.keys() for x in ['values', 'length']):
			self.data = np.hstack((kwargs.get("values"), kwargs.get("length")))
			self.length = kwargs.get("length")
			self.values = self.data[0]
			self.expectancies = self.data[1]

	def __add__(self, other):
		if isinstance(other, d):
			return self.addDice(other)
		elif isinstance(other, (int, float)):
			return d(self.values + other, self.expectancies, self.length)

	def __radd__(self, other):
		return self + other

	def __mul__(self, other):
		if isinstance(other, int):
			return self.times(other)

	def __rmul__(self, other):
		return self * other

	def __lt__(self, other):
		if isinstance(other, int):
			return

	def __gt__(self, other):
		return

	def __le__(self, other):
		return

	def __ge__(self, other):
		return

	def __str__(self):
		return "dice: " + str(self.values)

	def addDice(self, other):
		newLength = self.length + other.length - 1
		newValues = np.arange(self.values[0] + other.values[0], self.values[-1] + other.values[-1] + 1)
		newExpectancies = np.zeros((newLength,))
		for i in np.arange(self.length):
			newExpectancies[i:i + other.length] += (self.expectancies[i] * other.expectancies)
		newExpectancies = d.normalize(newExpectancies)
		return d(newValues, newExpectancies, newLength)

	def times(self, factor):
		if factor == 0:
			return d(0)
		elif factor == 1:
			return self
		else:
			return self + self.times(factor - 1)

	def meanValueWeighted(self):
		return np.average(self.values, weights=self.expectancies)

	def meanValueAndExpectancy(self):
		index = self.meanIndex()
		data = np.vstack((self.values, self.expectancies))
		valueBounds = self.values[np.floor(index):np.floor(index) + 2]
		value = valueBounds[0] + (index % 1) * valueBounds[1] - valueBounds[0]
		expectancyBounds = self.expectancies[np.floor(index):np.floor(index) + 2]
		expectancy = expectancyBounds[0] + (index % 1) * expectancyBounds[1] - expectancyBounds[0]
		return value, expectancy

	def meanIndex(self):
		return np.average(np.arange(self.length), weights=self.expectancies)

	def normalizeExpectancies(self):
		self.expectancies = d.normalize(self.expectancies)

	@staticmethod
	def normalize(expectancies):
		return expectancies / np.sum(expectancies)

	def plot(self):
		plot(self)


def plot(dice):
	xdata = dice.values
	ydata = dice.expectancies * 100

	meanVal, meanExp = dice.meanValueAndExpectancy()

	plt.plot(meanVal, meanExp * 100, 'ro')

	plt.plot(xdata, ydata)

	plt.xlabel('dice rolls')
	plt.ylabel('likelihood (in percent)')
	plt.title('DnDice')
	plt.grid(True)

	# plt.savefig("test.png")
	plt.show()


def byRoll(*args, **kwargs):
	if kwargs.get("for"):
		pass
