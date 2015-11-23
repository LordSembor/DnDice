__author__ = 'piMoll, Lord_sembor'

from d import d
import numpy as np


def main():
	try:
		damageRoll = (d(8) + 7 * d(6) + 3) * 3
		damageRoll.plot()
	except MemoryError:
		print("'(d(8)+7*d(6)+3)*3' failed\n")
	print(np.sort((3 * d(6)).values))
	hit = 3 * d(3)
	crit = 7 * d(2)
	index = np.where(hit.values == crit.values[0], 1, 0)
	print(index[0])


if __name__ == '__main__':
	main()
