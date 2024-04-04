import os
import copy

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from ipgm.proportional import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *

MUNICIPALITY = 'marseille'
SEATS_DATA_FILE = 'sectors_2020'
DIVS_DATA_FILE = 'lyon_2020' if MUNICIPALITY == 'lyon' else 'paris' if MUNICIPALITY == 'paris' else 'marseille_2020' if MUNICIPALITY == 'marseille' else MUNICIPALITY
SEATS_SCALE = 3 if MUNICIPALITY == 'lyon' else 6

#Get divs data
#with open(f'data/{municipality}/rings/arrondissements.csv','r',encoding='utf8') as seatsDataFile:
#	ringsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
#	ringsData = {x[0]: dict(zip(ringsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in ringsDataTemp[1:]}

#Get seats data
with open(f'data/{MUNICIPALITY}/seats/{SEATS_DATA_FILE}.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsDataSectors = {x[0]: dict(zip(seatsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in seatsDataTemp[1:]}
seatsPerSector = {k: v['seats'] for k,v in seatsDataSectors.items()}

allDivs = AllDivs(f'data/{MUNICIPALITY}/divs/{DIVS_DATA_FILE}.txt')

t1_2020 = importDataTable(f'data/{MUNICIPALITY}/stats/2020T1.csv', allDivs)
t2_2020 = importDataTable(f'data/{MUNICIPALITY}/stats/2020T2.csv', allDivs)

candidaciesData: Candidacies = importCandidacies(src=f'data/{MUNICIPALITY}/cands/2020.csv')



seatsPartiesSectorsT1 = {x: proportionalHighestAverage(filterThreshold(t1_2020.get(x), 0), seatsPerSector[x], divisor=getDHondtDivisor) for x in allDivs.allDivs if x in seatsPerSector}

seatsPartiesSectorsT2 = {x: PLMProportional(filterThreshold(t2_2020.get(x), 0.05), seatsPerSector[x]) for x in allDivs.allDivs if x in seatsPerSector}
if MUNICIPALITY == 'paris': #first round
	seatsPartiesSectorsT2['A07'] = {'LR': 4}

print('Arrondissements proportional T1:')
print(sortedDict(cleanDict(
	{k: sum( [x[k] if k in x else 0 for x in seatsPartiesSectorsT1.values()] ) for k in [x.shortName for x in candidaciesData.listOfCands]}
), reverse=True))
print((seatsPartiesSectorsT1))

print('Arrondissements proportional T2:')
print(sortedDict(cleanDict(
	{k: sum( [x[k] if k in x else 0 for x in seatsPartiesSectorsT2.values()] ) for k in [x.shortName for x in candidaciesData.listOfCands]}
), reverse=True))
print((seatsPartiesSectorsT2))



#exportMap(t1_2020, f'data/{municipality}/maps/bureaux_de_vote_2020.svg', f'seats/2020T1_{MUNICIPALITY}_b.svg', candidaciesData=candidaciesData)
#exportMap(t1_2020, f'data/{municipality}/maps/quartiers.svg',            f'seats/2020T1_{MUNICIPALITY}_q.svg', candidaciesData=candidaciesData)
#exportMap(t1_2020, f'data/{municipality}/maps/arrondissements.svg',      f'seats/2020T1_{MUNICIPALITY}_a.svg', candidaciesData=candidaciesData)
exportSeatsMap(t1_2020, seatsPartiesSectorsT1, seatsDataSectors, f'data/{MUNICIPALITY}/maps/secteurs.svg', f'seats/2020T1_{MUNICIPALITY}_as.svg', allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=SEATS_SCALE)

#exportMap(t2_2020, f'data/{municipality}/maps/bureaux_de_vote_2020.svg', f'seats/2020T2_{MUNICIPALITY}_b.svg', candidaciesData=candidaciesData)
#exportMap(t2_2020, f'data/{municipality}/maps/quartiers.svg',            f'seats/2020T2_{MUNICIPALITY}_q.svg', candidaciesData=candidaciesData)
#exportMap(t2_2020, f'data/{municipality}/maps/arrondissements.svg',      f'seats/2020T2_{MUNICIPALITY}_a.svg', candidaciesData=candidaciesData)
exportSeatsMap(t2_2020, seatsPartiesSectorsT2, seatsDataSectors, f'data/{MUNICIPALITY}/maps/secteurs.svg', f'seats/2020T2_{MUNICIPALITY}_as.svg', allDivs=allDivs, candidaciesData=candidaciesData, seatsScale=SEATS_SCALE)

