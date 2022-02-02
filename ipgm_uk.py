import os
from copy import *

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from ipgm.proportional import *
from ipgm.Candidacies import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *

#Get seats data
with open('data/seats_uk.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsDataRegions = {x[0]: {'seats': int(x[1]), 'layout': x[2], 'orientation': x[3], 'cx': toFloat(x[4]), 'cy': toFloat(x[5])} for x in seatsDataTemp[1:]}
seatsPerRegion = {k: v['seats'] for k,v in seatsDataRegions.items()}

with open('data/seats_uk_counties.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsDataCounties = {x[0]: {'seats': int(x[1]), 'layout': x[2], 'orientation': x[3], 'cx': toFloat(x[4]), 'cy': toFloat(x[5])} for x in seatsDataTemp[1:]}
seatsPerCounty = {k: v['seats'] for k,v in seatsDataCounties.items()}





allDivs = AllDivs('data/divs_uk.txt')

t = loadDataTable('data/stats_uk/2019GE.csv', allDivs)

poll = 'uk/RaWS_20220117'

mx = importMatricesJson('data/pollDefs/{0}.json'.format(poll))
if not os.path.exists('exports/{path}'.format(path=poll)):
	os.makedirs('exports/{path}'.format(path=poll))

candidaciesData: Candidacies = importCandidacies(srcParties='data/parties_uk.csv', srcCandidates='data/candidates_uk.csv')

doExportTxt = True
doExportMap = True
doExportCsv = True

doExportPropMap = True

allRounds = {}
allSeats = {}
allTexts = []

for hk, hv in {k: v for k,v in mx.items() if k != 'sampleSize'}.items():
	tn = int(hk[0])

	if tn == 1:
		r = extrapolateResults(t, hv['matrix_2019GE_2024GE'.format(h=hk)])
		r1 = deepcopy(r)
	else:
		r = extrapolateResults(r1, hv['matrix_2019GE_2024R2'.format(h=hk)])

	curScores = hv[('scores_2024{0}'.format('GE' if tn == 1 else 'R2').format(h=hk))]
	for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
		r = redressementResults(r, curScores[i], weight=(1 if i == 'Great Britain' else 0.5))
	
	if tn == 1: r.replaceCand('Scotland', 'Green', 'Scottish Greens')
	
	seatsPartiesRegions = {x: proportionalHighestAverage(filterThreshold(r.get(x), 0.05), seatsPerRegion[x], 'D\'Hondt') for x in allDivs.allDivs if x in seatsPerRegion}
	seatsPartiesCounties = {x: proportionalHighestAverage(filterThreshold(r.get(x), 0.05), seatsPerCounty[x], 'D\'Hondt') for x in allDivs.allDivs if x in seatsPerCounty}

	#Put it in allRounds
	allRounds[hk] = r
	allSeats[hk] = (seatsPartiesRegions, seatsPartiesCounties)
	
	#Tweet text
	if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.get('Great Britain').toPercentages(), hv['sampleSize'], top=1, candidaciesData=candidaciesData, nbSimulated=15000))

	#Export and map
	if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r)
	if doExportMap:
		exportMap(r, 'data/basemap_gb_counties_simplified.svg', '{path}/{h}.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData, mapScaling=2, sameParty=r.get('Great Britain').checkEqualParty(candidaciesData))
		if doExportPropMap and tn == 1:
			exportSeatsMap(r, seatsPartiesRegions, seatsDataRegions, 'data/basemap_gb_regions.svg', '{path}/{h}_prop_r.svg'.format(h=hk, path=poll), allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=0.6, mapScaling=3, sameParty=r.get('Great Britain').checkEqualParty(candidaciesData))
			exportSeatsMap(r, seatsPartiesCounties, seatsDataCounties, 'data/basemap_gb_counties_merged.svg', '{path}/{h}_prop_c.svg'.format(h=hk, path=poll), allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=0.6, mapScaling=3, sameParty=r.get('Great Britain').checkEqualParty(candidaciesData))


if doExportTxt:
	with open('exports/{path}/tweetText.txt'.format(path=poll),'w',encoding='utf8') as txtFile:
		txtFile.write('\n\n'.join(allTexts))

print('Regional proportional:')
print(sortedDict(cleanDict({k: sum([x[k] if k in x else 0 for x in allSeats['1_GE'][0].values()]) for k in candidaciesData.getAllCands()}), reverse=True))

print('County proportional:')
print(sortedDict(cleanDict({k: sum([x[k] if k in x else 0 for x in allSeats['1_GE'][1].values()]) for k in candidaciesData.getAllCands()}), reverse=True))
