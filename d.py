from . import plot as dndplot
import math
import numpy as np

__author__ = 'sam <vogelsangersamuel@hotmail.com>, piMoll'


# noinspection PyPep8Naming
class d(object):
	def __init__(self, *args, **kwargs):
		if len(args) == 0:
			self.__data = np.array([[], []])
			self.length = 0
		elif len(args) == 1:
			faces = args[0]
			if faces > 0:
				self.__data = np.array([np.arange(faces) + 1, np.ones(faces) / faces])
				self.length = faces
			else:
				self.__data = np.array([[0], [1]])
				self.length = 1
		elif len(args) == 2:
			self.__data = args[0]
			self.length = args[1]
		elif len(args) == 3:
			self.__data = np.vstack((args[0], args[1]))
			self.length = args[2]
		elif all(x in kwargs.keys() for x in ['values', 'length']):
			self.__data = np.vstack((kwargs.get("values"), kwargs.get("length")))
			self.length = kwargs.get("length")
		self.dice = kwargs.get('dice', [self])

	def __add__(self, other):
		if isinstance(other, d):
			return self.__add_dice(other)
		elif isinstance(other, (int, float)):
			return d(self.v + other, self.e, self.length, dice=self.dice)

	def __radd__(self, other):
		return self + other

	def __mul__(self, other):
		if isinstance(other, int):
			return self.__times(other)

	def __rmul__(self, other):
		return self * other

	def __iter__(self):
		return iter(np.swapaxes(self.__data, 0, 1))

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

	def __add_dice(self, other):
		new_length = self.length + other.length - 1
		new_values = np.arange(self.v[0] + other.v[0], self.v[-1] + other.v[-1] + 1)

		new_expectancies = np.zeros((new_length,))
		for i in np.arange(self.length):
			new_expectancies[i:i + other.length] += (self.e[i] * other.e)

		return d(new_values, new_expectancies, new_length, dice=self.dice+other.dice)

	def __times(self, factor):
		if factor == 0:
			return d(0)
		elif factor == 1:
			return self
		else:
			return self.__add_dice(self.__times(factor - 1))

	@DeprecationWarning  # Currently not used
	def mean_value_weighted(self):
		return np.average(self.values(), weights=self.expectancies())

	def mean_value_and_expectancy(self):
		index = self.mean_index()
		index_int = np.floor(index)

		values = self.values()
		value_bounds = values[index_int:index_int + 2]
		value = value_bounds[0] + (index % 1) * (value_bounds[1] - value_bounds[0])

		expectancies = self.expectancies()
		expectancy_bounds = expectancies[index_int:index_int + 2]
		expectancy = expectancy_bounds[0] + (index % 1) * (expectancy_bounds[1] - expectancy_bounds[0])

		return value, expectancy

	def mean_index(self):
		return np.average(np.arange(self.length), weights=self.expectancies())

	def mean_and_std_dev(self):
		"""
		Return the weighted average and standard deviation.

		values, weights -- Numpy ndarrays with the same shape.
		"""
		values = self.values()
		weights = np.nan_to_num(self.expectancies())
		average = np.average(values, weights=weights)
		variance = np.average((values - average) ** 2, weights=weights)  # Fast and numerically precise
		return average, math.sqrt(variance)

	def normalize_expectancies(self):
		self.__data[1] = d.normalize(self.expectancies())

	@staticmethod
	def normalize(expectancies):
		return expectancies / np.sum(np.nan_to_num(expectancies))

	def plot(self, *args, draw_mean=False):
		if len(args) > 1:
			raise ValueError('Too many arguments')
		if len(args) == 1:
			plot_args = self, args[0]
		else:
			plot_args = self
		dndplot.plot(plot_args, draw_mean=draw_mean)

	def values(self):
		return self.__data[0]

	def expectancies(self):
		return np.nan_to_num(self.__data[1])

	def single(self, index=0):
		return self.dice[index]

	def layer(self, other, weight=1):
		if not isinstance(other, d):
			if isinstance(other, (int, float)):
				other = d([other], [1], 1)
			else:
				raise TypeError("Can only layer other dice")

		if self.length > 0:
			min_val = min(self.values().min(), other.values().min())
			max_val = max(self.values().max(), other.values().max())
		else:
			min_val = other.values().min()
			max_val = other.values().max()

		new_values = np.arange(min_val, max_val + 1)
		new_length = np.max(new_values.shape)
		new_expectancies = np.empty(new_length)
		new_expectancies.fill(np.NAN)

		other_index = np.where(new_values == other.values()[0])[0][0]
		new_expectancies[other_index:other.length + other_index] = (other.expectancies() * weight)

		if self.length > 0:
			self_index = np.where(new_values == self.values()[0])[0][0]
			new_expectancies[self_index:self.length + self_index] = \
				np.nan_to_num(new_expectancies[self_index:self.length + self_index]) + self.expectancies()
				# TODO: this overwrites the initial self NaN's, that shouldn't happen

		new_data = np.vstack((new_values, new_expectancies))
		self.__data = new_data
		self.length = new_length

if __name__ == '__main__':
	with open('README.md', 'r') as readme:
		print(readme.read())
