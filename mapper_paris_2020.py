import os
import copy

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *

#Get divs data
#with open('data/paris/rings/arrondissements.csv','r',encoding='utf8') as seatsDataFile:
#	ringsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
#	ringsData = {x[0]: dict(zip(ringsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in ringsDataTemp[1:]}

allDivs = AllDivs('data/paris/divs/paris.txt')

t1_2020 = importDataTable('data/paris/stats/2020T1.csv', allDivs)
#t2_2020 = importDataTable('data/paris/stats/2020T2.csv', allDivs)

candidaciesData: Candidacies = importCandidacies(src='data/paris/cands/2020.csv')

exportMap(t1_2020, 'data/paris/maps/bureaux_de_vote_2020.svg', 'Paris_2020/2020T1_b.svg', candidaciesData=candidaciesData)
exportMap(t1_2020, 'data/paris/maps/quartiers.svg',            'Paris_2020/2020T1_q.svg', candidaciesData=candidaciesData)
exportMap(t1_2020, 'data/paris/maps/arrondissements.svg',      'Paris_2020/2020T1_a.svg', candidaciesData=candidaciesData)

#Make individual maps for each party's scores (warning: very hacky bodge, candidates with a '#' at the start of their names are ignored for coloring purposes
candidatesList = ['PS', 'LR', 'LREM', 'EÉLV', 'NP', 'LFI', 'D-Goujon', 'RN', 'LO', 'PP', 'LP', 'SL', 'D-Espéronnier', 'D-Giazzi', 'D-Lécuyer', 'D-Lefort', 'I-Aoudia', 'POID', 'D-Tiberi', 'C-Baschet', 'D-Arnould', 'PC', 'UPR', 'I-Garnier', 'Volt', 'I-Préau']
for candidate in candidatesList:
	t1_2020.renameCandidate(candidate, '#'+candidate)

for candidate in candidatesList:
	t1_2020.renameCandidate('#'+candidate, candidate)
	scoreMultiplier = 0.5/t1_2020.result.toPercentages().results[candidate]
	exportMap(t1_2020, 'data/paris/maps/bureaux_de_vote_2020.svg', 'Paris_2020/{candidate}_b.svg'.format(candidate=candidate), candidaciesData=candidaciesData, scoreMultiplier=scoreMultiplier)
	exportMap(t1_2020, 'data/paris/maps/quartiers.svg',            'Paris_2020/{candidate}_q.svg'.format(candidate=candidate), candidaciesData=candidaciesData, scoreMultiplier=scoreMultiplier)
	exportMap(t1_2020, 'data/paris/maps/arrondissements.svg',      'Paris_2020/{candidate}_a.svg'.format(candidate=candidate), candidaciesData=candidaciesData, scoreMultiplier=scoreMultiplier)
	t1_2020.renameCandidate(candidate, '#'+candidate)