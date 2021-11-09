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
'Xavier Bertrand': Color('#0066cc'), #LR candidate
'Valérie Pécresse': Color('#0066cc'), #LR candidate
'Michel Barnier': Color('#0066cc'), #LR candidate
'Éric Ciotti': Color('#0066cc'), #LR candidate
'Philippe Juvin': Color('#0066cc'), #LR candidate
'Marine Le Pen': Color('#627cad'), #not same as wp
'Éric Zemmour': Color('#d99536'),

'François Fillon': Color('#0066cc'),
'Benoît Hamon': Color('#ff8080'),
'Nicolas Dupont-Aignan': Color('#8040c0'),
'Jean Lassalle': Color('#adc1fd'),
'Philippe Poutou': Color('#bb0000'),
'François Asselineau': Color('#118088'),
'Nathalie Arthaud': Color('#8e2f2f'),
'Jacques Cheminade': Color('#eedd00'), #to replace with orange

'Approuve': Color('#82bf40'),
'Désapprouve': Color('#bf409d'),
}



allDivs = AllDivs('data/divs_fr.txt')

t1 = loadDataTable('data/2017T1.csv')
t2 = loadDataTable('data/2017T2.csv')
te = loadDataTable('data/2019TE.csv')

mx = importMatrices('data/pollDefs/Ifop_20211105.polld')

doExportTxt = True
doExportMap = True
doExportCsv = True

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
	for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
	#for i in ['National']:
		r = redressementResults(r, curScores[i], allDivs=allDivs)
	
	#Put it in allRounds
	allRounds[hk] = r

	#Tweet text
	if doExportTxt: print('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.get('National', allDivs=allDivs).toPercentages(), hv['sampleSize'], top=(2 if tn==1 else 1)))

	#Export and map
	if doExportCsv: saveDataTable('exports/{h}.csv'.format(h=hk), r)
	if doExportMap: exportMap(r, 'data/basemap_collectivites.svg', '{h}_.svg'.format(h=hk), allDivs=allDivs, partiesColors=partiesColors)
	#if doExportMap: exportMap(r, 'data/basemap_depts.svg', '{h}.svg'.format(h=hk), allDivs=allDivs, partiesColors=partiesColors)

