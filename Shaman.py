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
	pass
