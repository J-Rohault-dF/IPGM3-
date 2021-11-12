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

electoralVotes = {
	'Ain': 8,
	'Aisne': 8,
	'Allier': 5,
	'Alpes-de-Haute-Provence': 3,
	'Hautes-Alpes': 3,
	'Alpes-Maritimes': 14,
	'Ardèche': 5,
	'Ardennes': 5,
	'Ariège': 3,
	'Aube': 5,
	'Aude': 5,
	'Aveyron': 5,
	'Bouches-du-Rhône': 24,
	'Calvados': 9,
	'Cantal': 4,
	'Charente': 5,
	'Charente-Maritime': 8,
	'Cher': 5,
	'Corrèze': 4,
	'Corse-du-Sud': 3,
	'Haute-Corse': 3,
	'Côte-d\'Or': 8,
	'Côtes-d\'Armor': 8,
	'Creuse': 3,
	'Dordogne': 6,
	'Doubs': 8,
	'Drôme': 7,
	'Eure': 8,
	'Eure-et-Loir': 7,
	'Finistère': 12,
	'Gard': 9,
	'Haute-Garonne': 15,
	'Gers': 4,
	'Gironde': 18,
	'Hérault': 13,
	'Ille-et-Vilaine': 12,
	'Indre': 4,
	'Indre-et-Loire': 8,
	'Isère': 15,
	'Jura': 5,
	'Landes': 5,
	'Loir-et-Cher': 5,
	'Loire': 10,
	'Haute-Loire': 4,
	'Loire-Atlantique': 15,
	'Loiret': 9,
	'Lot': 4,
	'Lot-et-Garonne': 5,
	'Lozère': 2,
	'Maine-et-Loire': 11,
	'Manche': 7,
	'Marne': 8,
	'Haute-Marne': 4,
	'Mayenne': 5,
	'Meurthe-et-Moselle': 10,
	'Meuse': 4,
	'Morbihan': 9,
	'Moselle': 14,
	'Nièvre': 4,
	'Nord': 32,
	'Oise': 11,
	'Orne': 5,
	'Pas-de-Calais': 19,
	'Puy-de-Dôme': 8,
	'Pyrénées-Atlantiques': 9,
	'Hautes-Pyrénées': 4,
	'Pyrénées-Orientales': 6,
	'Bas-Rhin': 14,
	'Haut-Rhin': 10,
	'Rhône': 6,
	'Métropole de Lyon': 15,
	'Haute-Saône': 4,
	'Saône-et-Loire': 8,
	'Sarthe': 8,
	'Savoie': 6,
	'Haute-Savoie': 9,
	'Paris': 30,
	'Seine-Maritime': 16,
	'Seine-et-Marne': 17,
	'Yvelines': 18,
	'Deux-Sèvres': 5,
	'Somme': 8,
	'Tarn': 5,
	'Tarn-et-Garonne': 4,
	'Var': 12,
	'Vaucluse': 8,
	'Vendée': 8,
	'Vienne': 6,
	'Haute-Vienne': 5,
	'Vosges': 6,
	'Yonne': 5,
	'Territoire de Belfort': 3,
	'Essonne': 15,
	'Hauts-de-Seine': 20,
	'Seine-Saint-Denis': 18,
	'Val-de-Marne': 17,
	'Val-d\'Oise': 15,
	'Guadeloupe': 7,
	'Martinique': 6,
	'Guyane': 4,
	'Réunion': 11,
	'Saint-Pierre-et-Miquelon': 3,
	'Mayotte': 3,
	'Saint-Martin': 1,
	'Saint-Barthélémy': 1,
	'Saint-Martin-et-Saint-Barthélémy': 1,
	'Wallis-et-Futuna': 2,
	'Polynésie-Française': 5,
	'Nouvelle-Calédonie': 4,
	'Français vivant hors de France': 23,
}



allDivs = AllDivs('data/divs_fr.txt')

#Load table
r = loadDataTable('exports/1_XB.csv')

#s = simulOneNat(r, 1.96, 1000, allDivs)
#showRes(s.get('National', allDivs))
#exportMap(s, 'basemap_collectivites.svg', 'stupidSim_.svg', allDivs=allDivs, partiesColors=partiesColors)

#Simulate many and export map
sm = simulMany(r, 1000, 4, 2000, allDivs=allDivs)
exportMapProbs(sm, 'data/basemap_collectivites.svg', 'manySims.svg', allDivs=allDivs, partiesColors=partiesColors)

#Compute potential electoral college (only doing 1ev per dept right now)
EV = {k: [0, 0, 0] for k in r.get('National', allDivs).getCandidates()}
EV['tossup'] = 0

for i in sm.keys():
	d = sm[i]
	k1, m = getProbsFromResDict(d)
	if i not in electoralVotes: continue
	if m > 0.9: EV[k1][0] += electoralVotes[i]
	elif m > 0.6: EV[k1][1] += electoralVotes[i]
	elif m > 0.3: EV[k1][2] += electoralVotes[i]
	else: EV['tossup'] += electoralVotes[i]

print(EV)