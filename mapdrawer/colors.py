import copy

from colour import Color

def getShadeFromIndex(color: Color, thisShade: int):
	numShades = 16
	#Inputs: 
	#-1: 5% (special)
	#0: 10% (special)
	#1: 15%
	#2: 20%
	#etc.
	#16: 90%
	thisShade -= 1
	
	color = copy.deepcopy(color)

	if -1 < thisShade < numShades:
		sn = numShades-1-thisShade
		color.luminance = (sn+0.5)/numShades
	elif thisShade == -1:
		color.luminance = 0.98125
	elif thisShade == -2:
		color.luminance = 0.9921875
	elif thisShade <= -3:
		color.luminance = 1
	elif thisShade == numShades+1:
		color.luminance = 0.015625
	elif thisShade >= numShades+2:
		color.luminance = 0
	return color

def getPartyColor(cand: str, partiesColors: dict) -> str:
	return partiesColors[cand]

def hasPartyColor(cand: str, partiesColors: dict) -> bool:
	return cand in partiesColors.keys()

def getShadeFromBrightness(color: Color, brightness: float):
	color = copy.deepcopy(color)
	color.set_luminance(brightness)
	return color