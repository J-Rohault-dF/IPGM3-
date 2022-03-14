from __future__ import annotations
from ipgm.Result import *
from ipgm.ResultPerc import *
from ipgm.Div import *
from ipgm.VTM import *



#Extrapolate ResultsSet based on a VTMatrix
def extrapolateResults(div: Div, changeMatrix: VTMatrix) -> Div:

	if div.subset == []:
		div.result = extrapolateResult(div.result, changeMatrix)
	else:
		for sd in div.subset:
			sd = extrapolateResults(sd, changeMatrix)
		div.recalculate()



#Extrapolate single Result based on a VTMatrix
def extrapolateResult(initialRes: Result, changeMatrix: VTMatrix) -> Result:
	allSumProducts = {cf: sumProductDict(initialRes.results, changeMatrix.getColDict(cf)) for cf in changeMatrix.final}
	allSumProducts = multiplyDict(allSumProducts, (initialRes.getSumOfVotes()/sumDict(allSumProducts)))
	return Result.fromLists(list(allSumProducts.keys()), list(allSumProducts.values()))



#Redressement per division
def redressementResults(div: Div, targetRes: ResultPerc, weight: float = 1) -> Div:

	#Propagate down to the target res
	if div.name != targetRes.name:
		return redressementResults(div.get(targetRes.name), targetRes, weight=weight)
	
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
			redressementResults(subdiv, subdiv.result.toPercentages().getAddedDict(diff), weight)
		
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





def averageResultsSet(*args: Div, superset: list[Div] = []) -> Div:
	if len(args) == 1: return args[0]
	
	if not allValuesEqual([x.name for x in args]): raise Exception('Attemps averaging different levels: {0}'.format([x.name for x in args]))

	#If at the bottom, then average
	if args[0].subset == []:
		return Div(superset, [], args[0].name, averageResults([x.result for x in args]))

	#Else, then send down then recalculate
	else:
		div = Div(superset, [], args[0].name, None)
		div.subset = [averageResultsSet([arg.get(x) for arg in args], div) for x in args[0].subset]
		return div



#Stupid debugging functions
def showRes(r: Result):
	r.toPercentages().removedAbs().display()
def showRess(d: Div, s: str):
	d.get(s).toPercentages().display()