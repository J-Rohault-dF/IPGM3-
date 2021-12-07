from ipgm.port import *
from ipgm.mainFuncs import *
from divsHandler import *
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
	'Jacques Cheminade': Color('#eedd00'), #to replace with orange

	'Arnaud Montebourg': Color('#cc6666'),
	'Fabien Roussel': Color('#dd0000'),
	'Jean-Christophe Lagarde': Color('#00ffff'),
	'Jean-Frédéric Poisson': Color('#0000ff'),
	'Florian Philippot': Color('#404040'),
}


#Get divs data
with open('data/rings_fr.csv','r',encoding='utf8') as seatsDataFile:
	ringsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	ringsData = {x[0]: dict(zip(ringsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in ringsDataTemp[1:]}

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
	'Saint-Martin et Saint-Barthélémy': 1,
	'Wallis-et-Futuna': 2,
	'Polynésie-Française': 5,
	'Nouvelle-Calédonie': 4,
	'Français vivant hors de France': 23,
}
abbr = {
	'Ain': 'AI',
	'Aisne': 'AN',
	'Allier': 'AL',
	'Alpes-de-Haute-Provence': 'AP',
	'Hautes-Alpes': 'HA',
	'Alpes-Maritimes': 'AM',
	'Ardèche': 'AR',
	'Ardennes': 'AD',
	'Ariège': 'AG',
	'Aube': 'AB',
	'Aude': 'AU',
	'Aveyron': 'AV',
	'Bouches-du-Rhône': 'RN',
	'Calvados': 'CV',
	'Cantal': 'CT',
	'Charente': 'CR',
	'Charente-Maritime': 'CM',
	'Cher': 'CH',
	'Corrèze': 'CZ',
	'Corse-du-Sud': 'CS',
	'Haute-Corse': 'HC',
	'Côte-d\'Or': 'CO',
	'Côtes-d\'Armor': 'CA',
	'Creuse': 'CE',
	'Dordogne': 'DD',
	'Doubs': 'DO',
	'Drôme': 'DR',
	'Eure': 'EU',
	'Eure-et-Loir': 'EL',
	'Finistère': 'FN',
	'Gard': 'GD',
	'Haute-Garonne': 'HG',
	'Gers': 'GE',
	'Gironde': 'GR',
	'Hérault': 'HE',
	'Ille-et-Vilaine': 'IV',
	'Indre': 'IN',
	'Indre-et-Loire': 'IL',
	'Isère': 'IS',
	'Jura': 'JR',
	'Landes': 'LN',
	'Loir-et-Cher': 'LC',
	'Loire': 'LO',
	'Haute-Loire': 'HL',
	'Loire-Atlantique': 'LA',
	'Loiret': 'LR',
	'Lot': 'LT',
	'Lot-et-Garonne': 'LG',
	'Lozère': 'LZ',
	'Maine-et-Loire': 'ML',
	'Manche': 'MN',
	'Marne': 'MA',
	'Haute-Marne': 'HM',
	'Mayenne': 'MY',
	'Meurthe-et-Moselle': 'MM',
	'Meuse': 'ME',
	'Morbihan': 'MR',
	'Moselle': 'MO',
	'Nièvre': 'NV',
	'Nord': 'ND',
	'Oise': 'OI',
	'Orne': 'OR',
	'Pas-de-Calais': 'PC',
	'Puy-de-Dôme': 'PY',
	'Pyrénées-Atlantiques': 'PR',
	'Hautes-Pyrénées': 'HP',
	'Pyrénées-Orientales': 'PO',
	'Bas-Rhin': 'BR',
	'Haut-Rhin': 'HR',
	'Rhône': 'RH',
	'Métropole de Lyon': 'LY',
	'Haute-Saône': 'HN',
	'Saône-et-Loire': 'SL',
	'Sarthe': 'SA',
	'Savoie': 'SV',
	'Haute-Savoie': 'VH',
	'Paris': 'PA',
	'Seine-Maritime': 'SM',
	'Seine-et-Marne': 'SE',
	'Yvelines': 'YV',
	'Deux-Sèvres': 'DS',
	'Somme': 'SO',
	'Tarn': 'TN',
	'Tarn-et-Garonne': 'GT',
	'Var': 'VR',
	'Vaucluse': 'VA',
	'Vendée': 'VD',
	'Vienne': 'VN',
	'Haute-Vienne': 'HV',
	'Vosges': 'VO',
	'Yonne': 'YO',
	'Territoire de Belfort': 'BL',
	'Essonne': 'ES',
	'Hauts-de-Seine': 'HS',
	'Seine-Saint-Denis': 'SD',
	'Val-de-Marne': 'VM',
	'Val-d\'Oise': 'VS',
	'Guadeloupe': 'GU',
	'Martinique': 'MT',
	'Guyane': 'GY',
	'Réunion': 'RE',
	'Saint-Pierre-et-Miquelon': 'PM',
	'Mayotte': 'YT',
	'Saint-Martin': 'ST',
	'Saint-Barthélémy': 'SB',
	'Saint-Martin et Saint-Barthélémy': 'MB',
	'Wallis-et-Futuna': 'WF',
	'Polynésie-Française': 'PL',
	'Nouvelle-Calédonie': 'NC',
	'Français vivant hors de France': 'EX',
}



allDivs = AllDivs('data/divs_fr.txt')

candidaciesData: Candidacies = importCandidacies(srcParties='data/parties_fr.csv', srcCandidates='data/candidates_fr.csv')

#Load table
r = loadDataTable('exports/fr/Ifop_20211206/1_VP.csv', allDivs)
r.trim(allDivs.firstLevel)

#s = simulOneNat(r, 1.96, 1000, allDivs)
#showRes(s.get('National', allDivs))
#exportMap(s, 'basemap_collectivites.svg', 'stupidSim_.svg', allDivs=allDivs, partiesColors=partiesColors)

#Simulate many and export map
sm = simulMany(r, 5000, 4, 2000, allDivs=allDivs)

#Compute potential electoral college
EV = {k: [0, 0, 0] for k in r.get('National').getCandidates()}
EV['tossup'] = {}

for i in sm.keys():
	d = sm[i]
	k1, m = getProbsFromResDict(d)
	if i not in electoralVotes: continue
	if m > 0.95: EV[k1][0] += electoralVotes[i]
	elif m > 0.80: EV[k1][1] += electoralVotes[i]
	elif m > 0.65: EV[k1][2] += electoralVotes[i]
	else:
		addInDict(EV['tossup'], 'between {0}'.format(andMergeSorted(getTopProbsFromDict(d, 0.8))), electoralVotes[i])
		#EV['tossup'] += electoralVotes[i]

print({k: v for k,v in EV.items() if v != [0,0,0]})

exportMapProbs(sm, 'data/basemap_collectivites_gparis.svg', 'manySims.svg', allDivs=allDivs, candidaciesData=candidaciesData, doRings=True, divsData=ringsData, outerRadius=(5*10), innerRadius=(3*10), doTexts=True, texts={k: '{0}\n{1}'.format(abbr[k], electoralVotes[k]) for k in ringsData.keys()}, fontSize=24, fontUsed='Century Gothic')
