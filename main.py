__author__ = 'piMoll, Lord_sembor'

import Shaman
from d import d
import numpy as np


def main():
	hit = 3 * d(3)
	crit = 7 * d(2)
	index = np.where(hit.values == crit.values[0], 1, 0)
	print(index)
	print(hit)
	print(crit)
	Shaman.experiment()


if __name__ == '__main__':
	main()
