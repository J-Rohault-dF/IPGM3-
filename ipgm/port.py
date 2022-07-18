import json
from pickletools import unicodestringnl
from ipgm.utils import *
from ipgm.Result import *
from ipgm.Div import *
from ipgm.VTM import *
from divsHandler import *

#Function to load a data table [FORMAT: CSV with SEMICOLONS]
def importDataTable(src: str, allDivs: AllDivs) -> Div:
	#Open the datatable and dump it into a python tab
	with open(src,'r',encoding='utf8') as dataTable:
		txt = dataTable.read()
		tab = [y.split(';') for y in [x for x in txt.split('\n')]]
	
	#Parse it and create the list of results
	if tab[-1] == '': tab = tab[:-1]
	listDivs: list[Div] = []
	for l in tab[1:]:
		listDivs.append(Div([], [], l[0], Result.fromLists(tab[0][1:], l[1:])))
	
	#Run through the divs to add the dependencies
	for k,v in allDivs.overLevel.items():
		
		over = findLambda(listDivs, k, lambda x: x.name)
		if over == None:
			over = Div([], [], k, Result())
			listDivs.append(over)

		for vv in v:
			under = findLambda(listDivs, vv, lambda x: x.name)
			if under == None:
				under = Div([], [], vv, Result())
				listDivs.append(under)
			over.insert(under)
	
	while over.superset != []:
		over = over.superset[0]
	
	over.recalculateAll()
	#Put the tab of results into NationalResults
	return over



def saveDataTable(src: str, dv: Div):
	ls = []
	next = []
	done = []
	ls.append(';'.join([''] + [str(x) for x in dv.result.results.keys()]))

	next.append(dv)
	while next != []: #For each div, add its results in ls and add its subdivs in next
		dv = next.pop()
		if dv.name in done: continue
		next += dv.subset
		ls.append(';'.join([dv.name] + [str(x) for x in dv.result.results.values()]))
		done.append(dv.name)

	with open(src, 'w', encoding='utf8') as exportFile:
		exportFile.write('\n'.join(ls))



def importMatricesJson(src: str):
	with open(src, 'r', encoding='utf8') as defsFile:
		obj = json.load(defsFile)
	
	allReturning = {}

	sampleSize = obj['sampleSize']

	for h in obj['hypotheses']:
		
		label = h['label']
		candidates = h['candidates']
		final = h['final']

		sampleSizeD = h['sampleSize'] if 'sampleSize' in h else None

		for m in h['matrices']:

			initials = [x for x in m['vtm'].keys()]
			finals = candidates if 'candidates' not in m else m['candidates'] #Pick hypothesis candidates except if matrix candidates override it
			transfersMatrix = [[float(y)/100 for y in x] for x in m['vtm'].values()]
			externalAbs = m['externalAbs']
			original = m['original']
			based_on = m['based_on'] if 'based_on' in m else None

			if based_on != None: appendDictInDict(allReturning, label, 'based_on', based_on)

			#Handle externalAbs
			if hasNonExpressed(final) and externalAbs:
				for l in transfersMatrix:
					scaling = sum([ (1 - l[finals.index(x)]) for x in allNonExpressed(finals) ])
					l = [v*scaling for k,v in dict(zip(finals,l)).items() if isExpressed(k)]

			vtm = VTMatrix(initials, finals, transfersMatrix)
			appendDictInDict(allReturning, label, 'matrix_{0}_{1}'.format(original, final), vtm)
		


		tt = h['totals']
		externalAbs = tt['externalAbs']
		scores = {}

		for tk,tv in tt['list'].items():

			d = dict(zip(candidates, [float(x)/100 for x in tv]))
			
			#Handle externalAbs (scale back the @)
			if hasNonExpressed(candidates) and externalAbs:
				scaling = sum([ (1 - d[x]) for x in allNonExpressed(candidates) ])
				d = {k2: v2*scaling if not isExpressed(k2) else v2 for k2,v2 in d.items()}
			
			scores[tk] = ResultPerc.fromVotelessDict(tk, d)
			
		appendDictInDict(allReturning, label, 'scores_{0}'.format(final), scores)

		appendDictInDict(allReturning, label, 'sampleSize', (sampleSizeD if sampleSizeD != None else sampleSize))
	


	return allReturning