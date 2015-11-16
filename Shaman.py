__author__ = 'sam <vogelsangersamuel@hotmail.com>'


class Shaman(object):
	def __init__(self, cleric, barbarian):
		pass

	def attack(self, attackRoll):
		if isinstance(attackRoll, d):
			result = d(0)
			for i in attackRoll:
				if attackRoll.values[i] > 18:
					crit = (d(8)+7*d(6))+d(8)+10
					result.stack(crit.values, crit.expectancies*attackRoll.expectancies[i])
				elif attackRoll.values[i] > 13:
					hit = d(8)+7*d(8)+10
					result.stack(hit.values, hit.expectancies*attackRoll.expectancies[i])
				else:
					result.stack(np.r_[0], np.r_[attackRoll.expectancies[i]])
			return result
