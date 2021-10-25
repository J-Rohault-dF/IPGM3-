import csv
import math
import xml.etree.ElementTree as etree
import os
import subprocess
from ipgm.ResultsSet import *
from mapdrawer.colors import *

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
    kp = d[k]
    indexInTable = math.floor(kp*20)-2

    if hasPartyColor(k, partiesColors):
        return getShade(getPartyColor(k, partiesColors), indexInTable).hex_l[1:]
    else:
        print('missing color for {0} ({1}%)'.format(k, kp))
        return '000000'

def getWinningColorR(res: Result, partiesColors: dict) -> str:
    if res == None: return '000000'
    else: return getWinningColor(res.toPercentages().removedAbs().results, partiesColors)





def exportMap(res: ResultsSet, mapSrc: str, mapTarget: str, allDivs: AllDivs, partiesColors: dict):
	mapTarget = 'exports/'+mapTarget

	with open(mapSrc, 'r', encoding='utf8') as originalMap:
		xmlR = etree.parse(originalMap)
	
	#Third, color in the final map
	with open(mapTarget,'w',encoding='utf8') as svg:
		#For each path:
		for i in xmlR.getroot().find('{http://www.w3.org/2000/svg}g'):
			#If id is in the deps list, replace the fill
			if i.get('id') in allDivs.allDivs:
				i.set('style', i.get('style').replace('000000', getWinningColorR(res.get(i.get('id'), allDivs=allDivs, quiet=True), partiesColors)))
					
		xmlR.write(mapTarget)
	
	print('inkscape --export-type=png {0}'.format(mapTarget))

	t = subprocess.run(['inkscape','--export-type=png','{0}'.format(mapTarget)], shell=True)

	print('Opening map...')
	os.system(mapTarget.replace('.svg','.png').replace('/','\\'))
