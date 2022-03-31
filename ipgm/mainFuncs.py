from __future__ import annotations
from ipgm.Result import *
from ipgm.ResultPerc import *
from ipgm.Div import *
from ipgm.VTM import *
import copy



#Extrapolate ResultsSet based on a VTMatrix
def extrapolateResults(odiv: Div, changeMatrix: VTMatrix) -> Div:
	div = copy.deepcopy(odiv)

	ls = div.recursiveSubres()
	for sd in ls:
		sd.result = extrapolateResult(sd.result, changeMatrix)
	
	div.recalculateAll()
	
	return div



#Extrapolate single Result based on a VTMatrix
def extrapolateResult(initialRes: Result, changeMatrix: VTMatrix) -> Result:
	allSumProducts = {cf: sumProductDict(initialRes.results, changeMatrix.getColDict(cf)) for cf in changeMatrix.final}
	allSumProducts = multiplyDict(allSumProducts, (initialRes.getSumOfVotes()/sumDict(allSumProducts)))
	return Result.fromLists(list(allSumProducts.keys()), list(allSumProducts.values()))



#Redressement per division
def redressementResults(div: Div, targetRes: ResultPerc, weight: float = 1) -> Div:

	#Propagate down to the target res
	if div.name != targetRes.name:
		redressementResults(div.get(targetRes.name), targetRes, weight=weight)
		return div

	#Compute the difference between the actual and target results
	actualRes: ResultPerc = div.result.toPercentages()
	diff: dict[str, float] = targetRes.getSubstracted(actualRes)

	diff = multiplyDict(diff, weight)

	if div.subset == []:
		#Compute the percentages then convert it back to results format
		percs: ResultPerc = div.result.toPercentages().getAddedDict(diff)
		percs.zipZeroes()
		div.result = Result.fromPercentages(percs)
	else:
		#For every subdivision:
		for subdiv in div.subset:
			redressementResults(subdiv, subdiv.result.toPercentages(subdiv.name).getAddedDict(diff), weight)
		
		div.recalculate()
	
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
		
		div.recalculate()
	
	return redressementResults(div, targetRes, weight=weight)





def averageDivs(divs: list[Div], superset: list[Div] = []) -> Div:
	print('Averaging:', divs)
	if len(divs) == 1: return divs[0]
	
	if not allValuesEqual([x.name for x in divs]): raise Exception('Attemps averaging different levels: {0}'.format([x.name for x in divs]))

	#Get the list and average
	divA = copy.deepcopy(divs[0])
	for dn in [x.name for x in divA.recursiveSubres()]:
		divA.get(dn).result = averageResults([x.result for x in divs])
	
	divA.recalculateAll()
	return divA



#Stupid debugging functions
def showRes(r: Result):
	r.toPercentages().removedAbs().display()
def showRess(d: Div, s: str):
	d.get(s).result.toPercentages().display()