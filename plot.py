import matplotlib.pyplot as plt


__author__ = 'sam'

def plot(*dice):
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
		_plot_single_die(color_index, (die, name))
		color_index = (color_index + 1) % len(color_list)
	plt.xlabel('dice rolls')
	plt.ylabel('likelihood (in percent)')
	plt.title('DnDice')
	plt.legend(loc='upper right')
	plt.grid(True)
	# plt.savefig("test.png")
	plt.show()


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


def _plot_single_die(color_index, die_data):
	die, name = die_data
	xdata = die.values()
	ydata = die.expectancies() * 100
	mean, std_dev = die.meanAndStdDev()
	label = '{name} ({mean:.2f}, {std:.2f})'.format(name=name, mean=mean, std=std_dev)
	plt.plot(
		xdata,
		ydata,
		color=color_list[color_index],
		label=label
	)
