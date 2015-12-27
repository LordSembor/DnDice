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
	single_result.normalize_expectancies()
	result = count * single_result
	return result


def single_attack(hit, crit, mod, prof, ac=14, attack_roll=d(20), gwm=False):

	if gwm and __get_gwm_decision(hit, mod, prof, ac, attack_roll):
		gwm_bonus = 10
		gwm_malus = 5
	else:
		gwm_bonus = 0
		gwm_malus = 0
	result = d()
	for val, prob in attack_roll:
		if (val + mod + prof - gwm_malus) >= ac:
			if val == 20:
				result.layer(crit + gwm_bonus, prob)
			else:
				result.layer(hit + gwm_bonus, prob)
		else:
			result.layer(d(0), prob)
	return result.normalize_expectancies()


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


def __get_gwm_decision(hit, mod, prof, ac, attack_roll):
	base_dmg, _ = hit.mean_value_and_expectancy()
	base_ar = ac - mod - prof
	max_base_dmg = __gwm_decision_data[attack_roll][base_ar]
	return base_dmg <= max_base_dmg


"""
Data by Xetheral from www.giantitp.com, posted in:
http://www.giantitp.com/forums/showthread.php?373572-GWM-Reference-Table
"""
__gwm_decision_data = {
	advantage(): {
		2:  104,
		3:  78,
		4:  61.09,
		5:  49.08,
		6:  40,
		7:  32.82,
		8:  26.95,
		9:  22,
		10: 17.74,
		11: 14,
		12: 10.67,
		13: 7.66,
		14: 4.9,
		15: 2.36,
		16: 2.87,
		17: 3.71,
		18: 5.42,
		19: 10.54,
		20: 9999
	},
	d(20): {
		2:  28,
		3:  26,
		4:  24,
		5:  22,
		6:  20,
		7:  18,
		8:  16,
		9:  14,
		10: 12,
		11: 10,
		12: 8,
		13: 6,
		14: 4,
		15: 2,
		16: 2.5,
		17: 3.33,
		18: 5,
		19: 10,
		20: 9999
	}
}
