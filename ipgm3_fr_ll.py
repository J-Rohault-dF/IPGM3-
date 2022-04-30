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
with open('data/rings_fr.csv','r',encoding='utf8') as seatsDataFile:
	ringsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	ringsData = {x[0]: dict(zip(ringsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in ringsDataTemp[1:]}

#Get seats data
with open('data/seats_fr_depts.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsData = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}
seatsPerDept = {k: v['seats'] for k,v in seatsData.items()}

allDivs = AllDivs('data/divs_fr.txt')

t1_2017 = loadDataTable('data/stats_fr/2017T1.csv', allDivs)
t2_2017 = loadDataTable('data/stats_fr/2017T2.csv', allDivs)
te_2019 = loadDataTable('data/stats_fr/2019TE.csv', allDivs)
t1_2022 = loadDataTable('data/stats_fr/2022T1.csv', allDivs)
t2_2022 = loadDataTable('data/stats_fr/2022T2.csv', allDivs)

poll = 'fr/Harris_20220425'

mx = importMatricesJson('data/pollDefs/{0}.json'.format(poll))
if not os.path.exists('exports/{path}'.format(path=poll)):
	os.makedirs('exports/{path}'.format(path=poll))

candidaciesData: Candidacies = importCandidacies(srcParties='data/parties_fr.csv', srcCandidates='data/candidates_fr.csv')



doExportTxt = True
doExportMap = True
doExportCsv = True

allRounds = {}
allTexts = []



for hk, hv in {k: v for k,v in mx.items() if k != 'sampleSize'}.items():

	#Extrapolate rs
	rl = []

	if 'matrix_2017T1_2022LL' in hv: rl.append(extrapolateResults(t1_2017, hv['matrix_2017T1_2022LL']))
	if 'matrix_2017T2_2022LL' in hv: rl.append(extrapolateResults(t2_2017, hv['matrix_2017T2_2022LL']))
	if 'matrix_2019TE_2022LL' in hv: rl.append(extrapolateResults(te_2019, hv['matrix_2019TE_2022LL']))
	if 'matrix_2022T1_2022LL' in hv: rl.append(extrapolateResults(t1_2022, hv['matrix_2022T1_2022LL']))
	if 'matrix_2022T2_2022LL' in hv: rl.append(extrapolateResults(t2_2022, hv['matrix_2022T2_2022LL']))

	rs = averageDivs(rl)

	#Redresse R1
	r = deepcopy(rs)
	curScores = hv[('scores_2022LL')]
	for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
		r = redressementResults(r, curScores[i], weight = (1 if i == 'National' else 0.75 if i == 'Province' else 0.5))
	
	#Put it in allRounds
	allRounds[hk] = r

	#Compute the seats count
	seatsParties = {x: proportionalHighestAverage(filterThreshold(r.get(x).result), seatsPerDept[x], 'D\'Hondt') for x in seatsPerDept.keys()}
	print(hk, {k: sum([xv[k] for xk,xv in seatsParties.items()]) for k,v in r.result.results.items() if isExpressed(k)})

	#Tweet text
	if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.result.toPercentages(), hv['sampleSize'], top=1, nbSimulated=15000, candidaciesData=candidaciesData, threshold=0.05))

	#Export and map
	if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r)
	if doExportMap:
		exportMap(r, 'data/basemap_collectivites_gparis.svg', '{path}/{h}.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData)
		exportMap(r, 'data/basemap_collectivites_gparis.svg', '{path}/{h}_r.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData, doRings=True, ringsData=ringsData, outerRadius=(5*10), innerRadius=(3*10))
		exportSeatsMap(r, seatsParties, seatsData, 'data/basemap_collectivites_gparis.svg', '{path}/{h}_s.svg'.format(h=hk, path=poll), allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=5, mapScaling=3)

if doExportTxt:
	with open('exports/{path}/tweetText.txt'.format(path=poll),'w',encoding='utf8') as txtFile:
		txtFile.write('\n\n'.join(allTexts))