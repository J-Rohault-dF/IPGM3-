import math
import xml.etree.ElementTree as etree
import os
import subprocess
from ipgm.ResultsSet import *
from mapdrawer.colors import *
from mapdrawer.seatsdrawer import *
from mapdrawer.keydrawer import *

def getMaxK(d):
	k = ''
	v = float('-inf')
	for i in d.keys():
		if d[i] > v:
			v = d[i]
			k = i
	return k

def getWinningColor(d: dict, partiesColors: dict) -> str:
	k = getMaxK(d)
	if k == '': k = getMaxK({k: v for i,v in d.items() if k != ''})
	kp = d[k]
	indexInTable = math.floor(kp*20)-2

	if k in partiesColors:
		return getShade(partiesColors[k], indexInTable).hex_l[1:]
	else:
		print('missing color for {0} ({1}%)'.format(k, kp))
		return '000000'

def getWinningColorR(res: Result, partiesColors: dict) -> str:
	if res == None: return '000000'
	else: return getWinningColor(res.toPercentages().removedAbs().results, partiesColors)

def getWinningColorP(d: dict[str, float], partiesColors: dict) -> str:
	if d == None: return '000000'

	k1, m = getProbsFromResDict(d)
	
	if m > 0.9: indexInTable = 11
	elif m > 0.6: indexInTable = 8
	elif m > 0.3: indexInTable = 5
	else: return '000000'

	if hasPartyColor(k1, partiesColors):
		return getShade(getPartyColor(k1, partiesColors), indexInTable).hex_l[1:]
	else:
		print('missing color for {0} ({1}%)'.format(k1, d[k1]))
		return '000000'





def mapColorerPercs(res: ResultsSet, allDivs: AllDivs, partiesColors: dict[str, Color], xmlR: etree.ElementTree):
	for i in xmlR.getroot().find('{http://www.w3.org/2000/svg}g'):
		#If id is in the deps list, replace the fill
		if i.get('id') in allDivs.allDivs:
			i.set('style', i.get('style').replace('000000', getWinningColorR(res.get(i.get('id'), allDivs=allDivs, quiet=True), partiesColors)))

def mapColorerProbs(probs: list[dict[str, float]], allDivs: AllDivs, partiesColors: dict[str, Color], xmlR: etree.ElementTree):
	for i in xmlR.getroot().find('{http://www.w3.org/2000/svg}g'):
		#If id is in the deps list, replace the fill
		if i.get('id') in allDivs.allDivs:
			i.set('style', i.get('style').replace('000000', getWinningColorP(probs[i.get('id')], partiesColors)))

def mapRinger(xmlL: etree.Element, xmlD: etree.Element, percs: dict[str, dict[str, float]], divsData: dict[str, dict[str, str|int]], outerRadius: float, innerRadius: float, partiesColors: dict[str, Color]):
	rings = etree.Element('{http://www.w3.org/2000/svg}g', attrib={'id': 'rings-{gid}'.format(gid=getRandomAlphanumeric(4))})

	for dk, dv in percs.items():
		dd = divsData[dk]

		parties = list(dv.keys())
		scores = [dv[x] for x in parties]
		colors = [partiesColors[x] for x in parties]

		rD, rR = drawPercRing((dd['cx'], dd['cy']), outerRadius, innerRadius, scores, colors)
		rBm, rB = drawPercRingBehind((dd['cx'], dd['cy']), innerRadius, outerRadius, (1/12))
		rR.insert(0, rB)

		rings.append(rR)
		xmlD.extend(rD)
		xmlD.extend(rBm)

	xmlL.append(rings)


def exportMap(res: ResultsSet, mapSrc: str, mapTarget: str, allDivs: AllDivs, partiesColors: dict[str, Color], doRings: bool = False, ringsData: dict[str, dict[str, str|int]] = {}, outerRadius: float = 0, innerRadius: float = 0):
	mapTarget = 'exports/'+mapTarget

	with open(mapSrc, 'r', encoding='utf8') as originalMap:
		xmlR = etree.parse(originalMap)
	
	mapColorerPercs(res, allDivs, partiesColors, xmlR)

	if doRings:
		mapRinger(xmlR.getroot().find('{http://www.w3.org/2000/svg}g'), xmlR.getroot().find('{http://www.w3.org/2000/svg}defs'), {x.name: x.toPercentages().removedAbs().results for x in res.listOfResults}, ringsData, outerRadius, innerRadius, partiesColors)
	
	xmlR.write(mapTarget)
	
	print('inkscape --export-type=png {0}'.format(mapTarget))

	t = subprocess.run(['inkscape','--export-type=png','{0}'.format(mapTarget)], shell=True)

	#print('Opening map...')
	#os.system(mapTarget.replace('.svg','.png').replace('/','\\'))



def exportMapProbs(probs: list[dict[str, float]], mapSrc: str, mapTarget: str, allDivs: AllDivs, partiesColors: dict):
	mapTarget = 'exports/'+mapTarget

	with open(mapSrc, 'r', encoding='utf8') as originalMap:
		xmlR = etree.parse(originalMap)
	
	mapColorerProbs(probs, allDivs, partiesColors, xmlR)
	
	xmlR.write(mapTarget)
	
	print('inkscape --export-type=png {0}'.format(mapTarget))
	t = subprocess.run(['inkscape','--export-type=png','{0}'.format(mapTarget)], shell=True)

	#print('Opening map...')
	#os.system(mapTarget.replace('.svg','.png').replace('/','\\'))



def exportSeatsMap(res: ResultsSet, seatsParties: dict[str, dict[str, int]], divsData: dict[str, dict[str, any]], mapSrc: str, mapTarget: str, allDivs: AllDivs, partiesColors: dict, scale: float = 1):
	mapTarget = 'exports/'+mapTarget

	with open(mapSrc, 'r', encoding='utf8') as originalMap:
		xmlR = etree.parse(originalMap)
	
	#Color in the map
	mapColorerPercs(res, allDivs, partiesColors, xmlR)

	#Put the seats & color them - TODO: Put this into its own function
	group = etree.Element('{http://www.w3.org/2000/svg}g', attrib={'id': 'allSeats-{id}'.format(id=getRandomAlphanumeric(4))})
	for i in xmlR.getroot().find('{http://www.w3.org/2000/svg}g'):
		#If id is in the deps list, put the seats
		if i.get('id') in seatsParties.keys():
			divName = i.get('id')
			c = drawCircles(divsData[divName], divName.replace(' ','-'), 2.2777781*scale, 0.569444*scale, 5.52238*scale)
			colorsSeats = [(partiesColors[k], v) for k,v in seatsParties[divName].items()]
			c = colorCircles(c, divName, colorsSeats)
			group.append(c)

	xmlR.getroot().find('{http://www.w3.org/2000/svg}g').append(group)
	
	xmlR.write(mapTarget)
	
	print('inkscape --export-type=png {0}'.format(mapTarget))
	t = subprocess.run(['inkscape','--export-type=png','{0}'.format(mapTarget)], shell=True)
	
	#print('Opening map...')
	#os.system(mapTarget.replace('.svg','.png').replace('/','\\'))