import os
from copy import *

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *
from ipgm.proportional import *

#Get divs data
with open('data/seats_fr_depts.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsData = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}
seatsPerDept = {k: v['seats'] for k,v in seatsData.items()}



allDivs = AllDivs('data/divs_fr.txt')

t1 = loadDataTable('data/stats_fr/2017T1.csv', allDivs)
t2 = loadDataTable('data/stats_fr/2017T2.csv', allDivs)

poll = 'fr/Elabe_20211220'

mx = importMatricesJson('data/pollDefs/{0}.json'.format(poll))
if not os.path.exists('exports/{path}'.format(path=poll)):
	os.makedirs('exports/{path}'.format(path=poll))

candidaciesData: Candidacies = importCandidacies(srcParties='data/parties_fr.csv', srcCandidates='data/candidates_fr.csv')

doExportTxt = True
doExportMap = True
doExportCsv = True

allRounds = {}
allTexts = []





#Compute data for the first round
hk,hv = '2022T1', mx['1_VP']
#Extrapolate rs
rl = []
if 'matrix_2017T1_2022T1' in hv: rl.append(extrapolateResults(t1, hv['matrix_2017T1_2022T1']))
if 'matrix_2017T2_2022T1' in hv: rl.append(extrapolateResults(t2, hv['matrix_2017T2_2022T1']))
rs = averageResultsSet(*rl)
#Redresse R1
rData = deepcopy(rs)
curScores = hv[('scores_2022T1')]
for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
	rData: ResultsSet = redressementResults(rData, curScores[i], weight = (1 if i == 'National' else 0.75 if i == 'Province' else 0.5))





for i in range(1):

	#Take the first round

	#Randomize it
	r1s = simulOneNat(rData, 1.96, 3000)

	#Depending on the top-2

	#Find the top-2 candidates
	top2 = sorted(r1s.get('National').results, reverse=True, key=lambda x: r1s.get('National').results[x])[0:2]
	top2 = sorted(top2) #Sort the candidates

	scenario = ''
	if top2 == ['Emmanuel Macron', 'Marine Le Pen']: scenario = 'EM_MLP'
	if top2 == ['Emmanuel Macron', 'Éric Zemmour']: scenario = 'EM_EZ'
	if top2 == ['Emmanuel Macron', 'Jean-Luc Mélenchon']: scenario = 'EM_JLM'
	if top2 == ['Emmanuel Macron', 'Valérie Pécresse']: scenario = 'EM_VP'
	hk,hv = '2022T2', mx['2_{0}'.format(scenario)]

	#Take the runoff transfers and compute the runoff
	rl = []
	if 'matrix_2017T1_2022T2' in hv: rl.append(extrapolateResults(t1, hv['matrix_2017T1_2022T2']))
	if 'matrix_2017T2_2022T2' in hv: rl.append(extrapolateResults(t2, hv['matrix_2017T2_2022T2']))
	if 'matrix_2022T1_2022T2' in hv: rl.append(extrapolateResults(r1s, hv['matrix_2022T1_2022T2']))
	rs = averageResultsSet(*rl)
	
	r2s = deepcopy(rs)
	curScores = hv[('scores_2022T2')]
	for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
		r2s: ResultsSet = redressementResults(r2s, curScores[i], weight = (1 if i == 'National' else 0.75 if i == 'Province' else 0.5))
	
	#Compute the runoff
	r2s = simulOneNat(r2s, 1.96, 3000)

	#Do the proportional apportionment
	seatsTotal = {x: twoRoundProportional(r1s.get(x).results, r2s.get(x).results, seatsPerDept[x]) for x in allDivs.allDivs if x in seatsPerDept}
	
	#Tweet text
	#if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r2s.get('National').toPercentages(), hv['sampleSize'], top=(2 if tn==1 else 1), nbSimulated=15000, candidaciesData=candidaciesData, threshold=0.05))

	#Export and map
	if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r2s)
	if doExportMap:
		exportMap(r2s, 'data/basemap_collectivites_gparis.svg', '{path}/{h}.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData)
		exportSeatsMap(r2s, seatsTotal, seatsData, 'data/basemap_collectivites_gparis.svg', '{path}/{h}_seats.svg'.format(h=hk, path=poll), allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=5, mapScaling=3, sameParty=False)

if doExportTxt:
	with open('exports/{path}/tweetText.txt'.format(path=poll),'w',encoding='utf8') as txtFile:
		txtFile.write('\n\n'.join(allTexts))