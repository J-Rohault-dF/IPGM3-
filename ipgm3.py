import os
from copy import *

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



print('test0')
	

allDivs = AllDivs('data/divs_fr.txt')

t1 = loadDataTable('data/stats_fr/2017T1.csv', allDivs)
t2 = loadDataTable('data/stats_fr/2017T2.csv', allDivs)
te = loadDataTable('data/stats_fr/2019TE.csv', allDivs)

print('test1')

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

print('test2')

for hk, hv in {k: v for k,v in mx.items() if k != 'sampleSize'}.items():
	tn = int(hk[0])

	#Extrapolate rs
	rl = []
	if tn == 1:
		if 'matrix_2017T1_2022T1' in hv: rl.append(extrapolateResults(t1, hv['matrix_2017T1_2022T1']))
		if 'matrix_2017T2_2022T1' in hv: rl.append(extrapolateResults(t2, hv['matrix_2017T2_2022T1']))
		if 'matrix_2019TE_2022T1' in hv: rl.append(extrapolateResults(te, hv['matrix_2019TE_2022T1']))
	elif tn == 2:
		if 'matrix_2017T1_2022T2' in hv: rl.append(extrapolateResults(t1, hv['matrix_2017T1_2022T2']))
		if 'matrix_2017T2_2022T2' in hv: rl.append(extrapolateResults(t2, hv['matrix_2017T2_2022T2']))
		if 'matrix_2019TE_2022T2' in hv: rl.append(extrapolateResults(te, hv['matrix_2019TE_2022T2']))
		if 'matrix_2022T1_2022T2' in hv: rl.append(extrapolateResults(allRounds[hv['based_on']], hv['matrix_2022T1_2022T2']))
	rs = averageResultsSet(*rl)

	print('test3')
	
	#Redresse R1
	r = deepcopy(rs)
	curScores = hv[('scores_2022T{n}'.format(n=tn))]
	for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
		r = redressementResults(r, curScores[i], weight = (1 if i == 'National' else 0.75 if i == 'Province' else 0.5))
	
	print('test4')
	
	#Put it in allRounds
	allRounds[hk] = r

	#Tweet text
	if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.get('National').toPercentages(), hv['sampleSize'], top=(2 if tn==1 else 1), nbSimulated=15000, candidaciesData=candidaciesData, threshold=0.05))

	print('test5')
	
	#Export and map
	if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r)
	if doExportMap:
		exportMap(r, 'data/basemap_collectivites_gparis.svg', '{path}/{h}.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData)
		exportMap(r, 'data/basemap_collectivites_gparis.svg', '{path}/{h}_r.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData, doRings=True, ringsData=ringsData, outerRadius=(5*10), innerRadius=(3*10))

if doExportTxt:
	with open('exports/{path}/tweetText.txt'.format(path=poll),'w',encoding='utf8') as txtFile:
		txtFile.write('\n\n'.join(allTexts))