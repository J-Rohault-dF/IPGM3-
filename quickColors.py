from mapdrawer.mapper import *

for i in range(25, 55, 5):
	print(i, getShade(Color('#4c88a9'), math.floor((i/100+0.01)*20)-2).hex_l[1:])
