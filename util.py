from .d import d
import numpy as np


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


def advantage(dice=d(20)):
	return highest_of(2*dice)


def disadvantage(dice=d(20)):
	return lowest_of(2*dice)


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
	expectancies = __roll_count(dice_count, faces)
	values = np.arange(1, faces + 1)
	return values, expectancies, faces


def __roll_count(dice_count, faces):
	counts = np.arange(0, faces + 1) ** dice_count
	expectancies = d.normalize(counts[1:] - counts[:-1])
	return expectancies
