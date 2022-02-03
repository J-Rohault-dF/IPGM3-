import os
from copy import *

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *

#Get divs data
with open('data/seats_fr.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsData = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}




allDivs = AllDivs('data/divs_fr.txt')

t1 = loadDataTable('data/stats_fr/2017T1.csv', allDivs)
t2 = loadDataTable('data/stats_fr/2017T2.csv', allDivs)
te = loadDataTable('data/stats_fr/2019TE.csv', allDivs)
parrainages = loadDataTable('data/stats_fr/parrainages.csv', allDivs)

#poll = 'fr/Elabe_20211220'

#mx = importMatricesJson('data/pollDefs/{0}.json'.format(poll))
#if not os.path.exists('exports/{path}'.format(path=poll)):
#	os.makedirs('exports/{path}'.format(path=poll))

candidaciesData: Candidacies = importCandidacies(srcParties='data/parties_fr.csv', srcCandidates='data/candidates_fr.csv')

doExportTxt = False
doExportMap = True
doExportCsv = True

allRounds = {}
allTexts = []


poll = 'fr/parrainages'
if not os.path.exists('exports/{path}'.format(path=poll)):
	os.makedirs('exports/{path}'.format(path=poll))


r = deepcopy(parrainages)
hk = 1

#Tweet text
if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.get('National').toPercentages(), 1000, top=2, nbSimulated=15000, candidaciesData=candidaciesData, threshold=0.05))

#Export and map
#if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r)
#if doExportMap:
#	exportMap(r, 'data/basemap_collectivites_gparis.svg', '{path}/{h}.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData)
#	exportMap(r, 'data/basemap_collectivites_gparis.svg', '{path}/{h}_r.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData, doRings=True, ringsData=seatsData, outerRadius=(5*10), innerRadius=(3*10))

for k,v in seatsData.items():
	if r.contains(k):
		v['seats'] = int(r.get(k).getSumOfVotes())
		r.get(k).sortByVotes(doRandom=True)
		seatsData[k] = v

if doExportTxt:
	with open('exports/{path}/tweetText.txt'.format(path=poll),'w',encoding='utf8') as txtFile:
		txtFile.write('\n\n'.join(allTexts))

#Export and map
if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r)
#exportMap(r, 'data/basemap_collectivites_gparis.svg', '{path}/{h}.svg'.format(h=hk, path=poll), candidaciesData=candidaciesData, mapScaling=2, sameParty=r.get('Great Britain').checkEqualParty(candidaciesData))
exportSeatsMap(r, r.exportDict(), seatsData, 'data/basemap_collectivites_parrainages.svg', '{path}/{h}_parrainages.svg'.format(h=hk, path=poll), allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=3, mapScaling=3, sameParty=False)
