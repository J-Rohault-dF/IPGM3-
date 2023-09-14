import copy
from ipgm.proportional import apparentementsProportional, filterThreshold, getHagenbachBischoffQuota, proportionalLargestRemainder

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *

allDivs = AllDivs('data/ch/divs/ch.txt')

nrw_2019 = importDataTable('data/ch/stats/2019NRW.csv', allDivs)

poll = 'ch/Sotomo_20230825'

#mx = importMatrices('data/ch/polls/{0}.json'.format(poll))
#if not os.path.exists('exports/{path}'.format(path=poll)):
#	os.makedirs('exports/{path}'.format(path=poll))

candidaciesData: Candidacies = importCandidacies(src='data/ch/cands/parties.csv')

#Get seats data
with open('data/ch/seats/cantons.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsDataCantons = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}
seatsPerCanton = {k: int(v['seats']) for k,v in seatsDataCantons.items()}


# Fix the fact that the 2019 results are in *suffrages*, not electors
nrw_2019.removeCandidate('@blank')
nrw_2019.removeCandidate('@invalid')
nrw_2019.removeCandidate('@abstension')

seatsPerCanton2019 = copy.deepcopy(seatsPerCanton)
seatsPerCanton2019['Kanton Basel-Stadt'] += 1; seatsPerCanton2019['Kanton Zürich'] -= 1

for canton,seats in seatsPerCanton2019.items():
	nrw_2019.get(canton).multiply(1/seats)

nrw_2019.recalculateAll()



doExportTxt = True
doExportMap = True
doExportCsv = True



#Redresse R1
nrw_2023 = copy.deepcopy(nrw_2019)
nrw_2023.mergeCandidates('BDP', 'CVP')
nrw_2023.renameCandidate('CVP', 'DM')
nrw_2023.renameCandidate('GPS', 'Grüne')
nrw_2023.renameCandidate('MCG', 'MCR')
nrw_2023.renameCandidate('Übrige', 'Others')
pollScores = ResultPerc.fromVotelessDict('Switzerland', {'SVP': 27.6, 'SP': 17.3, 'DM': 14.8, 'FDP': 14.6, 'Grüne': 10.7, 'GLP': 7.3, 'EVP': 2.1, 'EDU': 1.05, 'EàG': 1.05, 'Lega': 0.75, 'AL': 0.32, 'Piraten': 0.27, 'CSP': 0.26, 'MCR': 0.22, 'SD': 0.13, 'Others': 1.55})
nrw_2023 = redressementResults(nrw_2023, pollScores, weight = 1)
nrw_2023.renameCandidate('Others', '#Others')

apparentements = {
	x: [
		['SP', 'Grüne', 'EàG'],
		['DM', 'GLP', 'EVP', 'CSP'],
		['SVP', 'FDP', 'EDU', 'Lega', 'LPS'],
	]
	if x not in ['Kanton Uri', 'Kanton Obwalden', 'Kanton Nidwalden', 'Kanton Glarus', 'Kanton Appenzell Innerrhoden', 'Kanton Appenzell Ausserrhoden']
	else []
	for x in seatsPerCanton.keys()
}

#Tweet text
#if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.result.toPercentages(), hv['sampleSize'], top=(2 if tn==1 else 1), nbSimulated=15000, candidaciesData=candidaciesData, threshold=0.05))

#Compute the seats count
#for x in seatsPerCanton.keys():
#	print(nrw_2023.get(x))
seatsPartiesCantons = {
	canton: apparentementsProportional(filterThreshold(nrw_2023.get(canton).result), seatsPerCanton[canton], proportionalLargestRemainder, getHagenbachBischoffQuota, apparentements[canton])
	for canton in seatsPerCanton.keys()
}
#print(nrw_2023, 'seatsPartiesCantons', {k: sum([(xv[k] if k in xv else 0) for xk,xv in seatsPartiesCantons.items()]) for k,v in nrw_2023.result.results.items() if isCandidate(k)})

#Export and map
if doExportCsv: saveDataTable(f'exports/{poll}/c.csv', nrw_2023)
if doExportMap:
	#exportMap(nrw_2023, 'data/ch/maps/cantons.svg', f'{poll}/{"nrw_2023"}_r.svg', candidaciesData=candidaciesData, ringsData=ringsData, outerRadius=(5*10), innerRadius=(3*10))
	exportMap(nrw_2023, 'data/ch/maps/cantons.svg', f'{poll}/{"nrw_2023"}_cantons.svg', candidaciesData=candidaciesData)
	print('Canton map exported')
	exportMap(nrw_2023, 'data/ch/maps/districts.svg', f'{poll}/{"nrw_2023"}_districts.svg', candidaciesData=candidaciesData)
	print('District map exported')
	exportMap(nrw_2023, 'data/ch/maps/gemeinds.svg', f'{poll}/{"nrw_2023"}_gemeinds.svg', candidaciesData=candidaciesData)
	print('Gemeind map exported')
	exportSeatsMap(nrw_2023, seatsPartiesCantons, seatsDataCantons, 'data/ch/maps/cantons.svg', f'{poll}/nrw_2023_seats.svg', allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=3)
	print('Cantonal seats map exported')
