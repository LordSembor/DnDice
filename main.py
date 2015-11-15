__author__ = 'piMoll, Lord_sembor'


from d import d
import numpy as np

def main():
	try:
		damageRoll = (d(8)+7*d(6)+3)*3
		damageRoll.plot()
	except MemoryError:
		print("'(d(8)+7*d(6)+3)*3' failed\n")
	print(np.sort((3*d(6)).values))

if __name__ == '__main__':
	main()
