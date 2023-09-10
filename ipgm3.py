import os
import copy

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

allDivs = AllDivs('data/fr/divs/fr.txt')

t1_2022 = importDataTable('data/fr/stats/2022T1.csv', allDivs)
t2_2022 = importDataTable('data/fr/stats/2022T2.csv', allDivs)

poll = 'Ifop_20230331'

mx = importMatrices('data/fr/polls/{0}.json'.format(poll))
if not os.path.exists('exports/{path}'.format(path=poll)):
	os.makedirs('exports/{path}'.format(path=poll))

candidaciesData: Candidacies = importCandidacies(src='data/fr/cands/2027P.csv')



doExportTxt = True
doExportMap = True
doExportCsv = True

allRounds = {}
allTexts = []



for hk, hv in {k: v for k,v in mx.items() if k != 'sampleSize'}.items():
	tn = int(hk[0])

	#Extrapolate rs
	rl = []
	if tn == 1:
		if 'matrix_2022T1_2027T1' in hv: rl.append(extrapolateResults(t1_2022, hv['matrix_2022T1_2027T1']))
		if 'matrix_2022T2_2027T1' in hv: rl.append(extrapolateResults(t2_2022, hv['matrix_2022T2_2027T1']))
		#if 'matrix_2024TE_2027T1' in hv: rl.append(extrapolateResults(te_2019, hv['matrix_2019TE_2027T1']))
	elif tn == 2:
		if 'matrix_2022T1_2027T2' in hv: rl.append(extrapolateResults(t1_2022, hv['matrix_2022T1_2027T2']))
		if 'matrix_2022T2_2027T2' in hv: rl.append(extrapolateResults(t2_2022, hv['matrix_2022T2_2027T2']))
		#if 'matrix_2024TE_2027T2' in hv: rl.append(extrapolateResults(te_2019, hv['matrix_2019TE_2027T2']))
		#if 'matrix_2027T1_2027T2' in hv: rl.append(extrapolateResults(allRounds[hv['based_on']], hv['matrix_2027T1_2027T2']))
	rs = averageDivs(rl)

	#Redresse R1
	r = copy.deepcopy(rs)
	curScores = hv[('scores_2027T{n}'.format(n=tn))]
	for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
		r = redressementResults(r, curScores[i], weight = (1 if i == 'National' else 0.75 if i == 'Province' else 0.5))
	
	#Put it in allRounds
	allRounds[hk] = r

	#Tweet text
	if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.result.toPercentages(), hv['sampleSize'], top=(2 if tn==1 else 1), nbSimulated=15000, candidaciesData=candidaciesData, threshold=0.05))

	#Export and map
	if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r)
	if doExportMap:
		exportMap(r, 'data/fr/maps/depts.svg', '{path}/{h}.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData)
		exportMap(r, 'data/fr/maps/depts.svg', '{path}/{h}_r.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData, ringsData=ringsData, outerRadius=(5*10), innerRadius=(3*10))

if doExportTxt:
	with open('exports/{path}/tweetText.txt'.format(path=poll),'w',encoding='utf8') as txtFile:
		txtFile.write('\n\n'.join(allTexts))
