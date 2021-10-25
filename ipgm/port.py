from ipgm.utils import *
from ipgm.Result import *
from ipgm.ResultsSet import *
from ipgm.VTM import *
from collectivites import *

#Fonction pour charger un tableau de données en classe [FORMAT: CSV with SEMICOLONS]
def loadDataTable(src: str) -> ResultsSet:
	#Open the datatable and dump it into a python tab
	with open(src,'r',encoding='utf8') as dataTable:
		txt = dataTable.read()
		tab = [y.split(';') for y in [x for x in txt.split('\n')]]
	
	#Parse it and create the tab of results
	if tab[-1] == '': tab = tab[:-1]
	listResults = []
	for l in tab[1:]:
		listResults.append(Result.fromLists(l[0], tab[0][1:], l[1:]))
	
	#Put the tab of results into NationalResults
	return ResultsSet(listResults)



#Fonction pour exporter une classe NationalResults en tableau de pourcentages, retire automatiquement les '@'
def exportPercentages(src: str, natRes: ResultsSet, collectivites: list):
	candidates = list(natRes.get(collectivites[0]).results.keys())
	with open(src,'w',encoding='utf8') as exportFile:

		allLines = [';'.join([''] + [x for x in candidates if x != '@'])]
		
		for c in collectivites:
			#Check if the list of candidates is still the same
			if candidates != list(natRes.get(c).results.keys()):
				raise Exception('List of candidates has changed at {0}, from {1} to {2}'.format(c, candidates, list(natRes.get(c).results.keys())))
			else: candidates = list(natRes.get(c).results.keys())
			#Get the array of scores and add the line
			scores = percentList([v for k,v in natRes.get(c).results.items() if k != '@'])
			allLines.append(';'.join([str(x) for x in ([c] + scores)]))
		
		exportFile.write('\n'.join(allLines))

#Même qu'au-dessus, mais avec la liste de candidats pré-fournie
def exportPercentagesC(src: str, natRes: ResultsSet, collectivites: list, candidates: list):
	with open(src,'w',encoding='utf8') as exportFile:

		allLines = [';'.join([''] + candidates)]
		
		for c in collectivites:
			#Get the array of scores and add the line
			scores = percentList([v for k,v in natRes.get(c).results.items() if k in candidates])
			allLines.append(';'.join([str(x) for x in ([c] + scores)]))
		
		exportFile.write('\n'.join(allLines))



def importMatrices(src: str):
	with open(src,'r',encoding='utf8') as dataFile:
		allText = str(dataFile.read())

		candidates = []
		hypothesis = ''

		allReturning = {}

		#Split the thing by '-', for each component:
		for component in allText.split('/'):

			#Extract the contents and parse in arguments
			args = [x for x in component.split('\n') if (len(x) > 0 and x[0] in ['$', '#', '°', ';', ':', '§', '=', '¤'])]
			#Use exec() to create the variables

			#If it's (), define list of candidates
			#If it's [], define list of scores
			#If it's {}, define VTMatrix

			params = getArgs(args, '=')
			externalAbs = ('externalAbs' in params)
			#InternalAbs: given scores (including @) all sum to 100%, no change needed
			#ExternalAbs: only candidates' scores sum to 100%, they need to be scaled down (except @)

			if '(' in component:
				#List of candidates
				hypothesis = getArgs(args, '#')[0]
				candidates = getArgs(args, '§')[0].split(',')
				sampleSize = getArgs(args, '¤')[0]
				
				allReturning['candidates_{0}'.format(hypothesis)] = candidates
				allReturning['sampleSize'] = int(sampleSize)

			elif '[' in component:
				#List of scores
				hypothesis = getArgs(args, '#')[0]
				label = getArgs(args, '$')[0]
				scoreTable = dict([x.split(':') for x in getArgs(args, '°')])
				
				scores = {}
				#For each row in the list of scores:
				for k,v in scoreTable.items():
					#Format all the values
					d = dict(zip(candidates, [float(x)/100 for x in v.split(',')]))

					#Handle externalAbs (scale back the @)
					if '@' in candidates and externalAbs:
						scaling = (1 - d['@'])
						d = {k2: v2*scaling if (k2 != '@') else d['@'] for k2,v2 in d.items()}
					
					scores[k] = ResultPerc.fromVotelessDict(k, d)
				
				#scoreTable = {(k,[float(x) for x in v.split(',')]) for k,v in scoreTable.items()}
				allReturning['scores_{0}_{1}'.format(hypothesis, label)] = scores

			elif '{' in component:
				#VTMatrix
				hypothesis = getArgs(args, '#')[0]
				label = getArgs(args, '$')[0]
				transfers = getArgs(args, ';')
				
				transfersMatrix = [x.split(':')[1] for x in transfers]
				transfersMatrix = [[float(x)/100 for x in y.split(',')] for y in transfersMatrix]

				initials = [x.split(':')[0] for x in transfers]
				finals = getArgs(args, ':')[0].split(':')[1].split(',')

				#Handle externalAbs
				if '@' in candidates and externalAbs:
					for l in transfersMatrix:
						scaling = (1 - l[finals.index('@')])
						l = [v*scaling for k,v in dict(zip(finals,l)).items() if (k != '@')]
				
				vtm = VTMatrix(initials, finals, percentMatrix(transfersMatrix))
				allReturning['components_{0}_{1}'.format(hypothesis, label)] = vtm

		return allReturning