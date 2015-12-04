__author__ = 'sam <vogelsangersamuel@hotmail.com>'

from d import *
import numpy as np


class Shaman(object):
	def __init__(self):
		pass

	@staticmethod
	def roll():
		hit = d(8) + 7 * d(6) + 5
		crit = (d(8) + 7 * d(6)) * 2 + d(8) + 5
		attack = lambda roll: crit if roll > 18 else hit
		# d.where(d(20)>18,attack)
		return attack(1) + attack(1) + attack(1)


def test():
	hit = 3 * d(3)
	crit = 7 * d(2) + 3 + d(6) + 1
	print(hit)
	print(crit)


def experiment():
	print("\nShaman.py\n=========\n")
	stren = 3
	prof = 2
	hit = d(12) + stren
	crit = 3 * d(12) + stren
	attack = singleAttack(hit, crit, stren, prof, attackRoll=advantage())
	#  attack.plot()
	print(attack.meanValueAndExpectancy())
	print(attack.expectancies()[0])
	print(gwf(1).expectancies())
	d1and3 = d(np.r_[4], np.r_[1], 1)
	print(d1and3)
	print(d1and3.expectancies())


def singleAttack(hit, crit, mod, prof, ac=14, attackRoll=d(20)):
	result = d(0)
	for val, prob in attackRoll:
		if (val + mod + prof) >= ac:
			if val == 20:
				result.layer(crit, prob)
			else:
				result.layer(hit, prob)
		else:
			result.layer(d(0), prob)
	result.normalizeExpectancies()
	return result


def gwf(count=2, die=d(6)):
	result = d(0)
	for val, prob in die:
		if val < 3:
			result.layer(die)
		else:
			result.layer(d([val], [prob], 1))
	result.normalizeExpectancies()
	return count * result
