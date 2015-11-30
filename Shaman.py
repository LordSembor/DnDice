__author__ = 'sam <vogelsangersamuel@hotmail.com>'

from d import d
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

def experiment():
	print("\nShaman.py\n=========\n")
	str = 3
	prof = 2
	hit = d(12) + str
	crit = 3 * d(12) + str
	attack = singleAttack(hit, crit, str, prof)
	# attack.plot()

def singleAttack(hit, crit, mod, prof, ac=14, attackRoll=d(20)):
	result = d(0)
	for val, prob in attackRoll:
		if (val + mod + prof) >= ac:
			if val == 20:
				result += crit
			else:
				result += hit
		else:
			result += d(0)
	return result
