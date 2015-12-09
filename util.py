from .d import d
import numpy as np


def advantage(dice=d(20)):
	"""
	@:param d dice
	@:return d advantage
	"""
	if isinstance(dice, int):
		dice = d(dice)
	v = dice.expectancies()
	arr = np.ones((dice.length, dice.length)) * v
	arr = np.triu(arr, 0) + np.triu(arr, 1)
	expectancies = np.dot(v, arr)

	return d(dice.values(), expectancies, dice.length)


def gwf(dice=2*d(6)):
	single_result = d()
	count = len(dice.dice)
	die = dice.single()
	for val, prob in die:
		if val < 3:
			single_result.layer(die)
		else:
			single_result.layer(d([val], [1], 1))
	single_result.normalizeExpectancies()
	result = count * single_result
	return result


# TODO all this
# def highestNOf(n, dice):
# 	if isinstance(dice, int):
# 		dice = d(dice)
# 	dv = dice.values()
# 	values = n + np.arange(n * dv[0], n * dv[-1] + 1)
# 	for combination in permutation(dv[-1], n):
# 		pass
#
#
# def permutation(m, n):
# 	inds = np.indices((m,) * n)
# 	return inds.reshape(n, -1).T
