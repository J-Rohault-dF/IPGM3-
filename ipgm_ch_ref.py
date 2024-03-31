import copy
from ipgm.proportional import apparentementsProportional, filterThreshold, getHagenbachBischoffQuota, proportionalLargestRemainder

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *

allDivs = AllDivs('data/ch/divs/CH_2010.txt')

ref_main = importDataTable('data/ch/stats/20101128REF_main.csv', allDivs)

poll = 'ch/20101128REF'

#mx = importMatrices('data/ch/polls/{0}.json'.format(poll))
#if not os.path.exists('exports/{path}'.format(path=poll)):
#	os.makedirs('exports/{path}'.format(path=poll))

candidaciesData: Candidacies = importCandidacies(src='data/ch/cands/parties.csv')

#Get seats data
with open('data/ch/seats/cantons.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsDataCantons = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}
seatsPerCanton = {k: int(v['seats']) for k,v in seatsDataCantons.items()}


ref_main.removeCandidate('@Inv')
ref_main.removeCandidate('@Abs')

seatsPerCanton2019 = copy.deepcopy(seatsPerCanton)
seatsPerCanton2019['Kanton Basel-Stadt'] += 1; seatsPerCanton2019['Kanton Zürich'] -= 1

#ref_main.recalculateAll()



doExportTxt = True
doExportMap = True
doExportCsv = True



#Redresse R1
ref_main = copy.deepcopy(ref_main)

#Tweet text
#if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.result.toPercentages(), hv['sampleSize'], top=(2 if tn==1 else 1), nbSimulated=15000, candidaciesData=candidaciesData, threshold=0.05))

#Compute the seats count
#seatsPartiesCantons = {
#	canton: proportionalLargestRemainder(filterThreshold(ref_main.get(canton).result), seatsPerCanton[canton], getHagenbachBischoffQuota)
#	for canton in seatsPerCanton.keys()
#}

#Export and map
if doExportCsv: saveDataTable(f'exports/{poll}/c.csv', ref_main)
if doExportMap:
	#exportMap(ref_main, 'data/ch/maps/cantons.svg', f'{poll}/{"ref_main"}_r.svg', candidaciesData=candidaciesData, ringsData=ringsData, outerRadius=(5*10), innerRadius=(3*10))
	exportMap(ref_main, 'data/ch/maps/cantons.svg', f'{poll}/{"ref_main"}_cantons.svg', candidaciesData=candidaciesData)
	print('Canton map exported')
	exportMap(ref_main, 'data/ch/maps/districts_2023.svg', f'{poll}/{"ref_main"}_districts.svg', candidaciesData=candidaciesData)
	print('District map exported')
	exportMap(ref_main, 'data/ch/maps/gemeinds_2023.svg', f'{poll}/{"ref_main"}_gemeinds.svg', candidaciesData=candidaciesData)
	print('Gemeind map exported')
	#exportSeatsMap(ref_main, seatsPartiesCantons, seatsDataCantons, 'data/ch/maps/cantons.svg', f'{poll}/ref_main_seats.svg', allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=3)
	#print('Cantonal seats map exported')
