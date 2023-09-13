from ipgm.Result import *
from ipgm.ResultPerc import *
from ipgm.Div import *
from ipgm.VTM import *
import copy



#Extrapolate ResultsSet based on a VTMatrix
def extrapolateResults(odiv: Div, changeMatrix: VTMatrix) -> Div:
	div = copy.deepcopy(odiv)

	ls = div.allBaseSubDivs()
	for sd in ls:
		sd.result = extrapolateResult(sd.result, changeMatrix)
	
	div.recalculateAll()
	return div



#Extrapolate single Result based on a VTMatrix
def extrapolateResult(initialRes: Result, changeMatrix: VTMatrix) -> Result:
	allSumProducts = {cf: sumProductDict(initialRes.results, changeMatrix.getColDict(cf)) for cf in changeMatrix.final}
	
	if sumDict(allSumProducts) == 0: return initialRes
	
	allSumProducts = multiplyDict(allSumProducts, (initialRes.getSumOfVotes()/sumDict(allSumProducts)))
	return Result.fromLists(list(allSumProducts.keys()), list(allSumProducts.values()))



#Redressement per division
def redressementResults(div: Div, targetRes: ResultPerc, weight: float = 1) -> Div:

	#Propagate down to the target res
	if div.name != targetRes.name:
		redressementResults(div.get(targetRes.name), targetRes, weight=weight)
		return div

	div.recalculateAll()
	nationalVotes = div.result.getSumOfVotes()
	diffVotes = Result.fromPercentages(targetRes, nationalVotes).getSubstractedDict(div.result)

	diffVotes = multiplyDict(diffVotes, weight)

	if div.subset == []:
		div.result = div.result.addDict(diffVotes) #TODO: (Result).zipZeroes
		return div
	
	#todo: split allBaseSubDivs into those that *have* the party and those that don't, count votes for each, multiply diffV, add it
	#totalsPresent = {}
	#for subdiv in div.allBaseSubDivs():
	#	for party in subdiv.result.results.keys():
	#		if party not in totalsPresent:
	#			totalsPresent[party] = 0
	#		totalsPresent[party] += subdiv.result.getSumOfVotes()
	
	#For every subdivision:
	for subdiv in div.allBaseSubDivs():
		diffVotesLocal = multiplyDict(diffVotes, (subdiv.result.getSumOfVotes()/nationalVotes))
		subdiv.result = subdiv.result.addDict(diffVotesLocal)
	
	div.recalculateAll()
	return div



#Multiplying redressement per division
def redressementResultsMultiplicative(div: Div, targetRes: ResultPerc, weight: float = 1):

	#Propagate down to the target res
	if div.name != targetRes.name:
		return redressementResults(div.get(targetRes.name), targetRes, weight=weight)
	
	#Compute the difference between the actual and target results
	actualRes: ResultPerc = div.result.toPercentages()
	diff: dict[str, float] = targetRes.getDivided(actualRes)

	diff = multiplyDict(diff, weight)

	if div.subset == []:
		#Compute the percentages then convert it back to results format
		percs: ResultPerc = div.result.toPercentages().getMultipliedDict(diff)
		percs.zipZeroes()
		div.result = Result.fromPercentages(percs)
	else:
		#For every subdivision:
		for subdiv in div.subset:
			redressementResults(subdiv, subdiv.result.toPercentages().getMultipliedDict(diff), weight)
	
	div.recalculateAll()
	return redressementResults(div, targetRes, weight=weight)





#Stupid debugging functions
def showRes(d: Div):
	d.result.toPercentages(d.name).removedAbs().display()
def showRess(d: Div, s: str):
	d.get(s).result.toPercentages().display()