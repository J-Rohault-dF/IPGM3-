from ipgm.port import *
from ipgm.mainFuncs import *
from collectivites import *
from mapdrawer.mapper import *
from simulvote.simul import *



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
}



allDivs = AllDivs('data/divs_fr.txt')

#Load table
r = loadDataTable('exports/1_XB.csv')

#s = simulOneNat(r, 1.96, 1000, allDivs)
#showRes(s.get('National', allDivs))
#exportMap(s, 'basemap_collectivites.svg', 'stupidSim_.svg', allDivs=allDivs, partiesColors=partiesColors)

#Simulate many and export map
sm = simulMany(r, 1000, 4, 1000, allDivs=allDivs)
exportMapProbs(sm, 'data/basemap_collectivites.svg', 'manySims.svg', allDivs=allDivs, partiesColors=partiesColors)

#Compute potential electoral college (only doing 1ev per dept right now)
EV = {k: [0, 0, 0] for k in r.get('National', allDivs).getCandidates()}
EV['tossup'] = 0

for i in sm:
	d = sm[i]
	k1, m = getProbsFromResDict(d)
	if m > 0.9: EV[k1][0] += 1
	elif m > 0.6: EV[k1][1] += 1
	elif m > 0.3: EV[k1][2] += 1
	else: EV['tossup'] += 1
