import matplotlib.pyplot as plt


__author__ = 'sam'

def plot(*dice, draw_mean=False, show_plot=True):
	plt.figure(figsize=(16, 9), dpi=80)
	plt.rc(
		'lines',
		linewidth=3,
		marker='o',
		markersize=8,
		markeredgewidth=0,
	)

	color_index = 0
	dice_count = 1
	for die in dice:
		if isinstance(die, tuple):
			die, name = die
		else:
			name = "plot {}".format(dice_count)
			dice_count += 1
		__plot_single_die(color_index, (die, name), draw_mean=draw_mean)
		color_index = (color_index + 1) % len(color_list)

	plt.xlabel('dice rolls')
	plt.ylabel('likelihood (in percent)')
	plt.title('DnDice')
	plt.legend(loc='upper right')
	plt.grid(True)
	# plt.savefig("test.png")  # TODO: save plot support, save_plot=False
	if show_plot:
		plt.show()

"""
The HEX values of these colors are taken from Ethan Schoonover's Solarized theme (http://ethanschoonover.com/solarized)
"""
colors = {
	'yellow':   '#b58900',
	'orange':   '#cb4b16',
	'red':      '#dc322f',
	'magenta':  '#d33682',
	'violet':   '#6c71c4',
	'blue':     '#268bd2',
	'cyan':     '#2aa198',
	'green':    '#859900',
}


color_list = list(colors.values())


def __plot_single_die(color_index, die_data, draw_mean=False):
	die, name = die_data
	xdata = die.values()
	ydata = die.expectancies() * 100
	mean, std_dev = die.meanAndStdDev()
	label = '{name} ({mean:.2f}, {std:.2f})'.format(name=name, mean=mean, std=std_dev)
	color = color_list[color_index]
	plt.plot(
		xdata,
		ydata,
		color=color,
		label=label
	)
	if draw_mean:
		mean, mean_expectancy = die.meanValueAndExpectancy()
		plt.plot(
			mean,
			mean_expectancy * 100,
			color=color,
			markersize=9,
			markeredgewidth=1
		)
