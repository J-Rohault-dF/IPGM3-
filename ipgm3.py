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



allDivs = AllDivs('divs_fr.txt')

t1 = loadDataTable('2017T1.csv')
t2 = loadDataTable('2017T2.csv')

mx = importMatrices('Odoxa_20211020.polld')

#for hg in [('1_XB', ['2_EM_EZ', '2_EM_MLP', '2_EM_XB', '2_EM_JLM']), ('1_VP', ['2_EM_VP']), ('1_MB', [])]:
for hg in [('1_XB', []), ('1_XB_EZ', ['2_EM_MLP']), ('1_VP_EZ', []), ('1_MB_EZ', [])]:
	h = hg[0]

	#Extrapolate R1
	r1t1 = extrapolateResults(t1, mx['components_{h}_2017T1_2022T1'.format(h=h)])
	#r1t2 = extrapolateResults(t2, mx['components_{h}_2017T2_2022T1'.format(h=h)])
	#r1s = averageResultsSet(r1t1, r1t2, allDivs=allDivs)
	r1s = deepcopy(r1t1)

	#Redresse R1
	r1 = deepcopy(r1s)
	for i in ['National']:#['Région Parisienne', 'Nord-Est', 'Sud-Est', 'Sud-Ouest', 'Nord-Ouest', 'Province', 'National']:
		r1 = redressementResults(r1, mx['scores_{h}_2022T1'.format(h=h)][i], allDivs=allDivs)

	#Tweet text
	print('HYPOTHESIS {h}\n'.format(h=h)+makeTweetText(r1.get('National', allDivs=allDivs).toPercentages(), mx['sampleSize']))

	#Export and map
	#exportMap(r1, 'basemap_collectivites.svg', '{h}.svg'.format(h=h), allDivs=allDivs, partiesColors=partiesColors)



	for hh in hg[1]:
		#Extrapolate R1
		r2t1 = extrapolateResults(t1, mx['components_{h}_2017T1_2022T2'.format(h=hh)])
		#r2t2 = extrapolateResults(t2, mx['components_{h}_2017T2_2022T2'.format(h=hh)])
		r2r1 = extrapolateResults(r1, mx['components_{h}_2022T1_2022T2'.format(h=hh)])
		r2s = averageResultsSet(r2t1, r2r1, allDivs=allDivs)#, r2t2, r2r1, allDivs=allDivs)
		#r2s = deepcopy(r2r1)

		#Redresse R2
		r2 = deepcopy(r2s)
		for i in ['National']:#['Région Parisienne', 'Nord-Est', 'Sud-Est', 'Sud-Ouest', 'Nord-Ouest', 'Province', 'National']:
			r2 = redressementResults(r2, mx['scores_{h}_2022T2'.format(h=hh)][i], allDivs=allDivs)

		#Tweet text
		print('HYPOTHESIS {h}\n'.format(h=hh)+makeTweetText(r2.get('National', allDivs=allDivs).toPercentages(), mx['sampleSize']))

		#Export and map
		#exportMap(r2, 'basemap_collectivites.svg', '{h}.svg'.format(h=hh), allDivs=allDivs, partiesColors=partiesColors)

	print('\n\n')



#TODO:

#MAP   - Ajouter gestion automatique des couleurs
#TWEET - Ajouter simulation et calcul des probabilités
#MAYBE - Ajuster le programme pour exporter la participation ou les exprimés seulement
#MAYBE - Ajouter vérification régulière que sum de Results = 100% (par repondération après plus ou moins chaque étape, peut passer par une fonction de repondération de ResultsSet qui le fait pour chaque composant)

#DONE:
#Implémenter la lecture de matrices
#Mettre à jour les données pour remplacer le total des votes par le compte des non-exprimés (abstention, blancs, nuls)
#Ajouter les votes du second tour
#Ajuster la lecture de vtm pour prendre en compte le fait que l'abstention peut ne pas être comptée dans la liste des candidats (sum % > 100%)
#Ajouter export par toutes les otherCollectivites (peut-être juste avec un flattening ou un otherCollectivites.keys())
#Remplacer dicts de pourcentages par classe PercsResults ?
#Change vtm format and rename '.vtm' to '.polld' (for Poll Defs format)
#TWEET - Ajouter génération du tweet
#MAP   - Ajouter lecture directe du ResultsSet (au lien d'avoir à exporter en csv)
#MAP   - Ajouter Métropole de Lyon, et séparer Saint-Martin/Saint-Barthélémy
#      - CHANGE averageResultsSet TO WORK WITHOUT WEIGHTS AND WITH MORE THAN 2 RESULTSSETS







### DOCUMENTATION (BETA)

# loadDataTable(src): loads table of results from file in src [must remove totalcol before public]

# exportPercentages(src, t, divs): exports table of results to fil in src, from ResultsSet t and list of divs divs [must remove totalcol before public, may split into saveDataTable and exportPercentages based on whether it exports votes or percentages (latter would have an argument to choose if it saves turnout, all percentages, or only candidates)]

# importMatrices(src): imports list of candidates, results, and VTMatrices from file in src [needs full documentation and maybe reformatting of the .vtm format]



# extrapolateResults(t, m): extrapolates results of ResultsSet t using the VTMatrix m

# redressementResults(t, r, name): redresses the results in ResultsSet t for all divs in div name to the dict r

# averageResultsSet(t1, t2, <w1>, <w2>): averages the results in ResultsSets t1 and t2, using weights w1 and w2



# ResultsSet.getSumAll(): returns the national sum

"""enjeuxCouleurs = {
	'Pouvoir d\'achat': Color('#ff00ff'),
	'Protection sociale': Color('#ff8400'),
	'Sécurité': Color('#8e40bf'),
	'Immigration': Color('#0000ff'),
	'Lutte contre terrorisme': Color('#c7387b'),
	'Emploi': Color('#8fb34d'),
	'Environnement': Color('#00ff00'),
	'Inégalités sociales': Color('#ff0000'),
	'Éduation et formation': Color('#ffd500'),
	'Fiscalité': Color('#00ffff'),
	'Dette et déficits': Color('#bf4040'),
	'Logement': Color('#bf7940'),
	'Rôle de la France dans le monde': Color('#00a6ff'),
	'Construction européenne': Color('#c8ff00'),
	'Mondialisation': Color('#00ff95'),
	'Aucun': Color('#808080'),
}"""