__author__ = 'piMoll, Lord_sembor'

import Shaman
from d import d
import numpy as np


def main():
	hit = 3 * d(3)
	crit = 7 * d(2) + 3 + d(6) + 1
	print(hit)
	print(crit)
	Shaman.experiment()


if __name__ == '__main__':
	main()
