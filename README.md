# DnDice

This is a module that calculates and prints value-probabiliy distributions of dice rolls as commonly used in tabletop roleplay games such as 'Dungeon & Dragons®' (I haven't actually looked at what games other than D&D 5e might require.)

# Examples

This shows the basic dice rolling syntax, and how the probabilities are expressed. Notice that the +5 inside the gwf function is stripped:

```python
from DnDice import d, gwf

single_attack = 2*d(6) + 5
print(single_attack) # dice: [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

# don't do this:
wrong_way = gwf(2*d(6) + 5)
print(wrong_way) # dice: [2, 3, 4, 5, 6, 7, 8, ,9, 10, 11, 12]
# do this instead
great_weapon_fighting = gwf(2*d(6)) + 5
print(great_weapon_fighting) # dice: [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]

# comparison of the probability
print(single_attack.expectancies())
print(great_weapon_fighting.expectancies())
# [ 0.03,  0.06, 0.08, 0.11, 0.14, 0.17, 0.14, ...] (single attack)
# [0.003, 0.006, 0.03, 0.05, 0.10, 0.15, 0.17, ...] (gwf attack)
```

If you have cases where the dice rolled are dependent on a separate roll:

```python
from DnDice import d, advantage, plot

normal_hit = 1*d(12) + 5
critical_hit = 3*d(12) + 5

result = d()
for value, probability in advantage():
	if value == 20:
		result.layer(critical_hit, weight=probability)
	elif value + 5 >= 14:
		result.layer(normal_hit, weight=probability)
	else:
		result.layer(d(0), weight=probability)
result.normalizeExpectancies()

plot(
	(normal_hit, "normal hit"),
	(critical_hit, "critical hit"),
	(result, "weighted by an advantage d20")
)
```
![graph of normal and critical hit, and their weighted probabilities](/doc/img/weighting_example.png "graph of normal and critical hit, and their weighted probabilities")
