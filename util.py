from .d import d
import numpy as np


def advantage(dice=d(20)):
	"""
	@:param d dice
	@:return d advantage
	"""
	return highest_of(2*dice)


def gwf(dice=2*d(6)):
	single_result = d()
	count = len(dice.dice)
	die = dice.single()
	for val, prob in die:
		if val < 3:
			single_result.layer(die)
		else:
			single_result.layer(val)
	single_result.normalizeExpectancies()
	result = count * single_result
	return result


def highest_of(dice):
	v, e, l = __extrema_dice(dice)
	return d(v, e, l)


def lowest_of(dice):
	v, e, l = __extrema_dice(dice)
	return d(v, e[::-1], l)

def __extrema_dice(dice):
	if not isinstance(dice, d):
		raise ValueError
	dice_count = len(dice.dice)
	faces = dice.single().length
	helper = np.arange(0, faces+1)**dice_count
	counts = helper[1:] - helper[:-1]
	expectancies = counts * (1/faces)**dice_count
	values = np.arange(faces) + 1
	return values, expectancies, faces

