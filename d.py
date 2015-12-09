from . import plot
import math
import numpy as np

__author__ = 'sam <vogelsangersamuel@hotmail.com>, piMoll'


# noinspection PyPep8Naming
class d(object):
	def __init__(self, *args, **kwargs):
		if len(args) == 0:
			self.data = np.array([[], []])
			self.length = 0
		elif len(args) == 1:
			faces = args[0]
			if faces > 0:
				self.data = np.array([np.arange(faces) + 1, np.ones(faces)])
				self.normalizeExpectancies()
				self.length = faces
			else:
				self.data = np.array([[0], [1]])
				self.length = 1
		elif len(args) == 2:
			self.data = args[0]
			self.length = args[1]
		elif len(args) == 3:
			self.data = np.vstack((args[0], args[1]))
			self.length = args[2]
		elif all(x in kwargs.keys() for x in ['values', 'length']):
			self.data = np.vstack((kwargs.get("values"), kwargs.get("length")))
			self.length = kwargs.get("length")
		self.dice = kwargs.get('dice', [self])

	def __add__(self, other):
		if isinstance(other, d):
			return self.__addDice(other)
		elif isinstance(other, (int, float)):
			return d(self.v + other, self.e, self.length, dice=self.dice)

	def __radd__(self, other):
		return self + other

	def __mul__(self, other):
		if isinstance(other, int):
			return self.times(other)

	def __rmul__(self, other):
		return self * other

	def __iter__(self):
		return iter(np.swapaxes(self.data, 0, 1))

	def __lt__(self, other):      # TODO
		if isinstance(other, (int, float)):
			return np.where(self.values() > other, True, False)
		else:
			raise TypeError

	def __gt__(self, other):
		return      # TODO

	def __le__(self, other):
		return      # TODO

	def __ge__(self, other):
		return      # TODO

	def __str__(self):
		return "dice: " + str(self.values())

	def __getattr__(self, item):
		if item == 'v':
			return self.values()
		elif item == 'e' or item == 'p':
			return self.expectancies()
		else:
			raise AttributeError('Dndice.d has no such attribute')

	def __addDice(self, other):
		newLength = self.length + other.length - 1
		newValues = np.arange(self.v[0] + other.v[0], self.v[-1] + other.v[-1] + 1)

		newExpectancies = np.zeros((newLength,))
		for i in np.arange(self.length):
			newExpectancies[i:i + other.length] += (self.e[i] * other.e)
		# newExpectancies = d.normalize(newExpectancies)

		return d(newValues, newExpectancies, newLength, dice=self.dice + other.dice)

	def times(self, factor):
		if factor == 0:
			return d(0)
		elif factor == 1:
			return self
		else:
			return self.__addDice(self.times(factor - 1))

	@DeprecationWarning  # Currently not used
	def meanValueWeighted(self):
		return np.average(self.values(), weights=self.expectancies())

	def meanValueAndExpectancy(self):
		index = self.meanIndex()
		index_int = np.floor(index)

		values = self.values()
		valueBounds = values[index_int:index_int + 2]
		value = valueBounds[0] + (index % 1) * (valueBounds[1] - valueBounds[0])

		expectancies = self.expectancies()
		expectancyBounds = expectancies[index_int:index_int + 2]
		expectancy = expectancyBounds[0] + (index % 1) * (expectancyBounds[1] - expectancyBounds[0])

		return value, expectancy

	def meanAndStdDev(self):
		"""
		Return the weighted average and standard deviation.

		values, weights -- Numpy ndarrays with the same shape.
		"""
		values = self.values()
		weights = np.nan_to_num(self.expectancies())
		average = np.average(values, weights=weights)
		variance = np.average((values - average) ** 2, weights=weights)  # Fast and numerically precise
		return average, math.sqrt(variance)

	def meanIndex(self):
		return np.average(np.arange(self.length), weights=self.expectancies())

	def normalizeExpectancies(self):
		self.data[1] = d.normalize(self.expectancies())

	@staticmethod
	def normalize(expectancies):
		return expectancies / np.sum(np.nan_to_num(expectancies))

	def plot(self):
		plot.plot(self)

	def values(self):
		return self.data[0]

	def expectancies(self):
		return np.nan_to_num(self.data[1])

	def single(self, index=0):
		return self.dice[index]

	def layer(self, other, weight=1):
		if not isinstance(other, d):
			if isinstance(other, (int, float)):
				other = d([other], [1], 1)
			else:
				raise TypeError("Can only layer other dice")

		if self.length > 0:
			minVal = min(self.values().min(), other.values().min())
			maxVal = max(self.values().max(), other.values().max())
		else:
			minVal = other.values().min()
			maxVal = other.values().max()

		newValues = np.arange(minVal, maxVal + 1)
		newLength = np.max(newValues.shape)
		newExpectancies = np.empty(newLength)
		newExpectancies.fill(np.NAN)

		otherIndex = np.where(newValues == other.values()[0])[0][0]
		newExpectancies[otherIndex:other.length + otherIndex] = (other.expectancies() * weight)

		if self.length > 0:
			selfIndex = np.where(newValues == self.values()[0])[0][0]
			newExpectancies[selfIndex:self.length + selfIndex] = \
				np.nan_to_num(newExpectancies[selfIndex:self.length + selfIndex]) + self.expectancies()

		newData = np.vstack((newValues, newExpectancies))
		self.data = newData
		self.length = newLength

if __name__ == '__main__':
	with open('README.md', 'r') as readme:
		print(readme.read())
