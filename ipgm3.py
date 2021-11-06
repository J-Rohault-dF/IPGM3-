from copy import *

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from collectivites import *
from mapdrawer.mapper import *



partiesColors = {
'Jean-Luc Mélenchon': Color('#cc2443'),
'Yannick Jadot': Color('#00c000'),
'Anne Hidalgo': Color('#ff8080'),
'Emmanuel Macron': Color('#ffeb00'),
'Xavier Bertrand': Color('#0066cc'),
'Valérie Pécresse': Color('#0066cc'),
'Marine Le Pen': Color('#627cad'), #not same as wp
'Éric Zemmour': Color('#d99536'),

'François Fillon': Color('#0066cc'),
'Benoît Hamon': Color('#ff8080'),
'Nicolas Dupont-Aignan': Color('#8040c0'),
'Jean Lassalle': Color('#adc1fd'),
'Philippe Poutou': Color('#bb0000'),
'François Asselineau': Color('#118088'),
'Nathalie Arthaud': Color('#8e2f2f'),
'Jacques Cheminade': Color('#eedd00'),

'Approuve': Color('#82bf40'),
'Désapprouve': Color('#bf409d'),
}



allDivs = AllDivs('data/divs_fr.txt', ['Circonscription départementale du Rhône', 'Saint-Martin et Saint-Barthélémy'])

t1 = loadDataTable('data/2017T1.csv')
t2 = loadDataTable('data/2017T2.csv')
te = loadDataTable('data/2019TE.csv')

#r_test = t1.get('Rhône',allDivs).getAdded(t1.get('Métropole de Lyon',allDivs))
#r_test.name = 'Circonscription départementale du Rhône'
#t1.listOfResults.append(r_test)
#r_test2 = t1.get('Saint-Martin',allDivs).getAdded(t1.get('Saint-Barthélémy',allDivs))
#r_test2.name = 'Saint-Martin et Saint-Barthélémy'
#t1.listOfResults.append(r_test2)

mx = importMatrices('data/pollDefs/EZ-JLM_nonserious.polld')

doExportTxt = False
doExportMap = True
doExportCsv = False

allRounds = {}

for hk, hv in mx.items():
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
	rs = averageResultsSet(*rl, allDivs=allDivs)

	#Redresse R1
	r = deepcopy(rs)
	curScores = hv[('scores_2022T{n}'.format(n=tn))]
	#for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
	for i in ['National']:
		r = redressementResults(r, curScores[i], allDivs=allDivs)
	
	#Put it in allRounds
	allRounds[hk] = r

	#Tweet text
	if doExportTxt: print('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.get('National', allDivs=allDivs).toPercentages(), hv['sampleSize'], top=tn))

	#Export and map
	if doExportCsv: saveDataTable('exports/{h}.csv'.format(h=hk), r)
	if doExportMap: exportMap(r, 'data/basemap_collectivites.svg', '{h}.svg'.format(h=hk), allDivs=allDivs, partiesColors=partiesColors)
	#if doExportMap: exportMap(r, 'data/basemap_depts.svg', '{h}.svg'.format(h=hk), allDivs=allDivs, partiesColors=partiesColors)

