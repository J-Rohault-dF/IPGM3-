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

	'Arnaud Montebourg': Color('#cc6666'),
	'Fabien Roussel': Color('#dd0000'),
	'Jean-Christophe Lagarde': Color('#00ffff'),
	'Jean-Frédéric Poisson': Color('#0000ff'),
	'Florian Philippot': Color('#404040'),

	'Approuve': Color('#82bf40'),
	'Désapprouve': Color('#bf409d'),
}


#Get divs data
with open('data/rings_fr.csv','r',encoding='utf8') as seatsDataFile:
	ringsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	ringsData = {x[0]: dict(zip(ringsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in ringsDataTemp[1:]}




allDivs = AllDivs('data/divs_fr.txt')

t1 = loadDataTable('data/2017T1.csv')
t2 = loadDataTable('data/2017T2.csv')
te = loadDataTable('data/2019TE.csv')

poll = 'fr/Elabe_20211124'

mx = importMatricesJson('data/pollDefs/{0}.json'.format(poll))
if not os.path.exists('exports/{path}'.format(path=poll)):
	os.makedirs('exports/{path}'.format(path=poll))

doExportTxt = False
doExportMap = False
doExportCsv = False

allRounds = {}
allTexts = []

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
	rs = averageResultsSet(*rl, allDivs=allDivs)

	#Redresse R1
	r = deepcopy(rs)
	curScores = hv[('scores_2022T{n}'.format(n=tn))]
	for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
	#for i in ['National']:
		r = redressementResults(r, curScores[i], allDivs=allDivs, weight = (1 if i == 'National' else 0.75 if i == 'Province' else 0.5))
	
	#Put it in allRounds
	allRounds[hk] = r

	#Tweet text
	if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.get('National', allDivs=allDivs).toPercentages(), hv['sampleSize'], top=(2 if tn==1 else 1), nbSimulated=15000, threshold=0.05))

	#Export and map
	if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r, allDivs)
	if doExportMap:
		exportMap(r, 'data/basemap_collectivites_gparis.svg', '{path}/{h}.svg'.format(h=hk, path=poll), allDivs=allDivs, partiesColors=partiesColors)
		exportMap(r, 'data/basemap_collectivites_gparis.svg', '{path}/{h}_r.svg'.format(h=hk, path=poll), allDivs=allDivs, partiesColors=partiesColors, doRings=True, ringsData=ringsData, outerRadius=(5*10), innerRadius=(3*10))

if doExportTxt:
	with open('exports/{path}/tweetText.txt'.format(path=poll),'w',encoding='utf8') as txtFile:
		txtFile.write('\n\n'.join(allTexts))