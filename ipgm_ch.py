import os
from copy import *
from ipgm.proportional import filterThreshold, proportionalLargestRemainder

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *

allDivs = AllDivs('data/ch/divs/ch.txt')

nrw_2019 = importDataTable('data/ch/stats/2019NRW.csv', allDivs)

poll = 'ch/Leewas_20230726'

#mx = importMatrices('data/ch/polls/{0}.json'.format(poll))
#if not os.path.exists('exports/{path}'.format(path=poll)):
#	os.makedirs('exports/{path}'.format(path=poll))

candidaciesData: Candidacies = importCandidacies(src='data/ch/cands/parties.csv')

#Get seats data
with open('data/ch/seats/cantons.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsDataCantons = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}
seatsPerCanton = {k: v['seats'] for k,v in seatsDataCantons.items()}




doExportTxt = True
doExportMap = True
doExportCsv = True



#Redresse R1
nrw_2023 = deepcopy(nrw_2019)
nrw_2023.mergeCandidates('BDP', 'CVP')
nrw_2023.renameCandidate('CVP', 'DM')
nrw_2023.renameCandidate('GPS', 'Grüne')
pollScores = ResultPerc.fromVotelessDict('Switzerland', {'SVP': 27.9, 'SP': 17.3, 'FDP': 14.3, 'DM': 13.9, 'Grüne': 10.7, 'GLP': 8.2, 'EVP': 2.1, 'EDU': 1.05, 'EàG': 1.05, 'Lega': 0.75, 'AL': 0.32, 'Piraten': 0.27, 'CSP': 0.26, 'MCR': 0.22, 'SD': 0.13, 'Others': 1.55})
nrw_2023 = redressementResults(nrw_2023, pollScores, weight = 1)

apparentements = {
	x: [
		['SP', 'Grüne', 'EàG'],
		['SVP', 'FDP', 'EDU'],
		['DM', 'GLP', 'EVP'],
	] for x in seatsPerCanton.keys()
}

#Tweet text
#if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.result.toPercentages(), hv['sampleSize'], top=(2 if tn==1 else 1), nbSimulated=15000, candidaciesData=candidaciesData, threshold=0.05))

#Compute the seats count
#for x in seatsPerCanton.keys():
#	print(nrw_2023.get(x))
seatsPartiesCantons = {x: proportionalLargestRemainder(filterThreshold(nrw_2023.get(x).result), seatsPerCanton[x], 'Hagenbach-Bischoff') for x in seatsPerCanton.keys()}
print(nrw_2023, 'seatsPartiesCantons', {k: sum([(xv[k] if k in xv else 0) for xk,xv in seatsPartiesCantons.items()]) for k,v in nrw_2023.result.results.items() if isCandidate(k)})

#Export and map
if doExportCsv: saveDataTable('exports/{path}/c.csv'.format(path=poll), nrw_2023)
if doExportMap:
	#exportMap(nrw_2023, 'data/ch/maps/cantons.svg', '{path}/{h}.svg'.format(h=nrw_2023, path=poll), candidaciesData=candidaciesData)
	#exportMap(nrw_2023, 'data/ch/maps/cantons.svg', '{path}/{h}_r.svg'.format(h=nrw_2023, path=poll), candidaciesData=candidaciesData, ringsData=ringsData, outerRadius=(5*10), innerRadius=(3*10))
	exportSeatsMap(nrw_2023, seatsPartiesCantons, seatsDataCantons, 'data/ch/maps/cantons.svg', '{path}/c.svg'.format(path=poll), allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=5)

