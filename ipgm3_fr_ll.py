import os
from copy import *
from ipgm.proportional import *

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *

#Get divs data
with open('data/fr/rings/depts.csv','r',encoding='utf8') as seatsDataFile:
	ringsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	ringsData = {x[0]: dict(zip(ringsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in ringsDataTemp[1:]}

#Get seats data DEPTS
with open('data/fr/seats/depts.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsDataDepts = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}
seatsPerDept = {k: v['seats'] for k,v in seatsDataDepts.items()}

#Get seats data CONST
with open('data/fr/seats/canard.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsDataConst = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}
seatsPerConst = {k: v['seats'] for k,v in seatsDataConst.items()}

#Get seats data OLDREGIONS
with open('data/fr/seats/oldRegions.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsDataOldRegions = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}
seatsPerOldRegion = {k: v['seats'] for k,v in seatsDataOldRegions.items()}

#Get seats data REGIONS
with open('data/fr/seats/regions.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsDataRegions = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}
seatsPerRegion = {k: v['seats'] for k,v in seatsDataRegions.items()}

allDivs = AllDivs('data/fr/divs/prop.txt')

t1_2022 = importDataTable('data/fr/stats/2022T1.csv', allDivs)
t2_2022 = importDataTable('data/fr/stats/2022T2.csv', allDivs)

candidaciesData: Candidacies = importCandidacies('data/fr/cands/2027P.csv')



doExportTxt = False
doExportMap = True
doExportCsv = False

allRounds = {}
allTexts = []


poll = 'Elabe_20230405'
hk = '1_base'
sampleSize = 1808
r = importDataTable('exports/'+poll+'/'+hk+'.csv', allDivs)

#Compute the seats count
seatsPartiesDepts = {x: proportionalHighestAverage(filterThreshold(r.get(x).result), seatsPerDept[x], 'D\'Hondt') for x in seatsPerDept.keys()}
print(hk, 'seatsPartiesDepts', {k: sum([xv[k] for xk,xv in seatsPartiesDepts.items()]) for k,v in r.result.results.items() if isCandidate(k)})

seatsPartiesConst = {x: proportionalHighestAverage(filterThreshold(r.get(x).result), seatsPerConst[x], 'D\'Hondt') for x in seatsPerConst.keys()}
print(hk, 'seatsPartiesConst', {k: sum([xv[k] for xk,xv in seatsPartiesConst.items()]) for k,v in r.result.results.items() if isCandidate(k)})

seatsPartiesOldRegions = {x: proportionalHighestAverage(filterThreshold(r.get(x).result), seatsPerOldRegion[x], 'D\'Hondt') for x in seatsPerOldRegion.keys()}
print(hk, 'seatsPartiesOldRegions', {k: sum([xv[k] for xk,xv in seatsPartiesOldRegions.items()]) for k,v in r.result.results.items() if isCandidate(k)})

seatsPartiesRegions = {x: proportionalHighestAverage(filterThreshold(r.get(x).result), seatsPerRegion[x], 'D\'Hondt') for x in seatsPerRegion.keys()}
print(hk, 'seatsPartiesRegions', {k: sum([xv[k] for xk,xv in seatsPartiesRegions.items()]) for k,v in r.result.results.items() if isCandidate(k)})

#Tweet text
if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.result.toPercentages(), sampleSize, top=1, nbSimulated=15000, candidaciesData=candidaciesData, threshold=0.05))

#Export and map
if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r)
if doExportMap:
	#exportMap(r, 'data/fr/maps/collectivites_gparis.svg', '{path}/{h}.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData)
	#exportMap(r, 'data/fr/maps/collectivites_gparis.svg', '{path}/{h}_r.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData, doRings=True, ringsData=ringsData, outerRadius=(5*10), innerRadius=(3*10))
	exportSeatsMap(r, seatsPartiesDepts, seatsDataDepts, 'data/fr/maps/circonscriptions_depts.svg', '{path}/{h}_s_d.svg'.format(h=hk, path=poll), allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=5)
	exportSeatsMap(r, seatsPartiesConst, seatsDataConst, 'data/fr/maps/circonscriptions_canard.svg', '{path}/{h}_s_c.svg'.format(h=hk, path=poll), allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=5)
	exportSeatsMap(r, seatsPartiesOldRegions, seatsDataOldRegions, 'data/fr/maps/oldRegions.svg', '{path}/{h}_s_or.svg'.format(h=hk, path=poll), allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=5)
	exportSeatsMap(r, seatsPartiesRegions, seatsDataRegions, 'data/fr/maps/regions.svg', '{path}/{h}_s_r.svg'.format(h=hk, path=poll), allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=5)

if doExportTxt:
	with open('exports/{path}/tweetText.txt'.format(path=poll),'w',encoding='utf8') as txtFile:
		txtFile.write('\n\n'.join(allTexts))