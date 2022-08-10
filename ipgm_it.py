import os
from copy import *

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *

#Get divs data
#with open('data/nl/rings/provinces.csv','r',encoding='utf8') as seatsDataFile:
#	ringsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
#	ringsData = {x[0]: dict(zip(ringsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in ringsDataTemp[1:]}

print('Loading divs…')
allDivs = AllDivs('data/it/divs/comune2017.txt')

print('Importing results data…')
cd_2018 = importDataTable('data/it/stats/2018CD.csv', allDivs)
cd_2018 = redressementResults(cd_2018, ResultPerc('Italia', {'M5S': 0.3268, 'PD': 0.1876, 'Lega': 0.1735, 'FI': 0.1400, 'FdI': 0.0435, 'LeU': 0.0339, '+E': 0.0256, 'NcI-UDC': 0.0130, 'PaP': 0.0113, 'CasaPound': 0.0095, 'PdF': 0.0067,  'Insieme': 0.0058, 'CP': 0.0054, 'SVP-PATT': 0.0041, 'FN-FT': 0.0039, 'PC': 0.0033, 'PVU': 0.0015, '10VM': 0.0011, 'PCL-SCR': 0.0009, 'PRI-ALA': 0.0006, 'GN': 0.0006, 'AD': 0.0006, 'LdP': 0.0003, 'PpA': 0.0002, 'IR-DC': 0.0001, 'SiAmo': 0.0000, 'Renaissance-MIR': 0.0000, 'IaH': 0.0000}, totalVotes=None))

#poll = 'fr/Elabe_20220405'

#mx = importMatrices('data/nl/polls/{0}.json'.format(poll))
#if not os.path.exists('exports/{path}'.format(path=poll)):
#	os.makedirs('exports/{path}'.format(path=poll))

print('Importing candidacies data')
candidaciesData: Candidacies = importCandidacies(src='data/it/cands/parties.csv')
parties = [x.shortName for x in candidaciesData.listOfCands]

coalitions = {
    'CDX': ['FI', 'Lega', 'FdI', 'NcI-UDC', 'FI-FdI-MNVA'],
    'CSX': ['PD', '+E', 'Insieme', 'CP', 'VdA', 'PD-UV-UVP-EPAV'],
}

##Export 2018 parties map
print('Exporting 2018 parties map…')
exportMap(cd_2018, 'data/it/maps/2020_CD_Const.svg', 'it/cd_const.svg', candidaciesData=candidaciesData)
exportMap(cd_2018, 'data/it/maps/2020_CD_CP.svg', 'it/cd_cp.svg', candidaciesData=candidaciesData)

##Export 2018 coalitions map
print('Exporting 2018 coalitions map…')
cd_2018_c = deepcopy(cd_2018)
cd_2018_c.coalition(coalitions)
exportMap(cd_2018_c, 'data/it/maps/2020_CD_Const.svg', 'it/cd_const_c.svg', candidaciesData=candidaciesData)
exportMap(cd_2018_c, 'data/it/maps/2020_CD_CP.svg', 'it/cd_cp_c.svg', candidaciesData=candidaciesData)

#Export 2022 map
#dd = deepcopy(cd_2018)
#dd = redressementResults(dd, ResultPerc('Italia', {'M5S': 0.098, 'PD': 0.225, 'Lega': 0.134, 'FI': 0.083, 'FdI': 0.238,  'LeU': 0.042, '+E': 0.049, 'CP': 0.115}, None))
#dd.renameCandidate('CP', '#Oth')
#exportMap(dd, 'data/it/maps/2020_CD_Const.svg', 'it/cd_const_.svg', candidaciesData=candidaciesData)

#Export 2022 coalitions map
#dd_c = deepcopy(dd)
#dd_c.coalition(coalitions)
#exportMap(dd_c, 'data/it/maps/2020_CD_Const.svg', 'it/cd_const_c_.svg', candidaciesData=candidaciesData)

#exportMap(tk_2021, 'data/nl/maps/gemeinden_2021.svg', 'nl/tk_g.svg', candidaciesData=candidaciesData)
#exportMap(tk_2021, 'data/nl/maps/provinces.svg', 'nl/tk_p_r.svg', candidaciesData=candidaciesData, ringsData=ringsData, outerRadius=(5*10), innerRadius=(3*10))

#Get maps for the individual parties
#t = deepcopy(tk_2021)
#for i in [x for x in parties]: t.renameCandidate(i, '#'+i)
#for i in [x for x in parties]:
#	t.renameCandidate('#'+i, i)
#	print(i)
#	exportMap(t, 'data/nl/gemeinden_2021.svg', 'nl/g_'+i+'.svg', candidaciesData=candidaciesData, multiplier=(0.5/(tk_2021.result.results[i]/tk_2021.result.getSumOfVotes())))
#	t.renameCandidate(i, '#'+i)

#doExportTxt = True
#doExportMap = True
#doExportCsv = True
#
#allRounds = {}
#allTexts = []
#
#
#
#for hk, hv in {k: v for k,v in mx.items() if k != 'sampleSize'}.items():
#	tn = int(hk[0])
#
#	#Extrapolate rs
#	rl = []
#	if tn == 1:
#		if 'matrix_2017T1_2022T1' in hv: rl.append(extrapolateResults(t1_2017, hv['matrix_2017T1_2022T1']))
#		if 'matrix_2017T2_2022T1' in hv: rl.append(extrapolateResults(t2_2017, hv['matrix_2017T2_2022T1']))
#		if 'matrix_2019TE_2022T1' in hv: rl.append(extrapolateResults(te_2019, hv['matrix_2019TE_2022T1']))
#	elif tn == 2:
#		if 'matrix_2017T1_2022T2' in hv: rl.append(extrapolateResults(t1_2017, hv['matrix_2017T1_2022T2']))
#		if 'matrix_2017T2_2022T2' in hv: rl.append(extrapolateResults(t2_2017, hv['matrix_2017T2_2022T2']))
#		if 'matrix_2019TE_2022T2' in hv: rl.append(extrapolateResults(te_2019, hv['matrix_2019TE_2022T2']))
#		#if 'matrix_2022T1_2022T2' in hv: rl.append(extrapolateResults(allRounds[hv['based_on']], hv['matrix_2022T1_2022T2']))
#	rs = averageDivs(rl)
#
#	#Redresse R1
#	r = deepcopy(rs)
#	curScores = hv[('scores_2022T{n}'.format(n=tn))]
#	for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
#		r = redressementResults(r, curScores[i], weight = (1 if i == 'National' else 0.75 if i == 'Province' else 0.5))
#	
#	#Put it in allRounds
#	allRounds[hk] = r
#
#	#Tweet text
#	if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.result.toPercentages(), hv['sampleSize'], top=(2 if tn==1 else 1), nbSimulated=15000, candidaciesData=candidaciesData, threshold=0.05))
#
#	#Export and map
#	if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r)
#	if doExportMap:
#		exportMap(r, 'data/basemap_fr_collectivites_gparis.svg', '{path}/{h}.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData)
#		exportMap(r, 'data/basemap_fr_collectivites_gparis.svg', '{path}/{h}_r.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData, doRings=True, ringsData=ringsData, outerRadius=(5*10), innerRadius=(3*10))
#
#if doExportTxt:
#	with open('exports/{path}/tweetText.txt'.format(path=poll),'w',encoding='utf8') as txtFile:
#		txtFile.write('\n\n'.join(allTexts))
