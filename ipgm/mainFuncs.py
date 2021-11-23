from ipgm.Result import *
from ipgm.ResultsSet import *
from ipgm.ResultPerc import *
from ipgm.VTM import *



#Extrapolate ResultsSet based on a VTMatrix
def extrapolateResults(initialRes: ResultsSet, changeMatrix: VTMatrix) -> ResultsSet:
	finalRes = []

	#for every line in the results:
	for res in initialRes.listOfResults:
		finalRes.append(extrapolateResult(res, changeMatrix))

	return ResultsSet(finalRes)



#Extrapolate single Result based on a VTMatrix
def extrapolateResult(initialRes: Result, changeMatrix: VTMatrix) -> Result:
	allSumProducts = {cf: sumProductDict(initialRes.results, changeMatrix.getColDict(cf)) for cf in changeMatrix.final}
	allSumProducts = multiplyDict(allSumProducts, (initialRes.getSumOfVotes()/sumDict(allSumProducts)))
	return Result.fromLists(initialRes.name, list(allSumProducts.keys()), list(allSumProducts.values()))



#Redressement per division
def redressementResults(initialRes: ResultsSet, targetRes: ResultPerc, allDivs: AllDivs, weight: float = 1):
	fRes = []
	
	#Get all components
	targetName = targetRes.name
	targetDivisions: list[str] = unpackDivisions(targetName, allDivs.firstLevel, allDivs.overLevel)
	
	#Compute the difference between the actual and target results
	actualRes: ResultPerc = initialRes.sumIfs(targetDivisions).toPercentages(newName=targetName)
	diff: dict[str, float] = targetRes.getSubstracted(actualRes)

	diff = multiplyDict(diff, weight)

	#For every res in ResultsSet that is also contained in Result:
	for divName in initialRes.getAllDivs():
		res: Result = initialRes.get(divName, allDivs=allDivs)
		
		if divName in targetDivisions:

			#Compute the percentages then convert it back to results format
			percs: ResultPerc = res.toPercentages().getAddedDict(diff)
			percs.zipZeroes()
			fRes.append(Result.fromPercentages(percs))
		
		else:
			fRes.append(res)
	
	return ResultsSet(fRes)



#Multiplying redressement per division
def redressementResultsMultiplicative(initialRes: ResultsSet, targetRes: ResultPerc, allDivs: AllDivs, weight: float = 1):
	fRes = []
	
	#Get all components
	targetName = targetRes.name
	targetDivisions: list[str] = unpackDivisions(targetName, allDivs.firstLevel, allDivs.overLevel)
	
	#Compute the multiplicative difference between the actual and target results
	actualRes: ResultPerc = initialRes.sumIfs(targetDivisions).toPercentages(newName=targetName)
	diff: dict[str, float] = targetRes.getDivided(actualRes)

	diff = multiplyDict(diff, weight)

	#For every res in ResultsSet that is also contained in Result:
	for divName in initialRes.getAllDivs():
		res: Result = initialRes.get(divName, allDivs=allDivs)
		
		if divName in targetDivisions:

			#Compute the percentages then convert it back to results format
			percs: ResultPerc = res.toPercentages().getMultipliedDict(diff, True)
			percs.zipZeroes()
			fRes.append(Result.fromPercentages(percs))
		
		else:
			fRes.append(res)
	
	#Redresse the results linearly and return
	return redressementResults(ResultsSet(fRes), targetRes, allDivs=allDivs)



#Average multiple ResultsSets (for example average multiple redressements)
def averageResultsSet(*args: ResultsSet, allDivs: AllDivs) -> ResultsSet:
	fRes = []

	curDivs = []
	for i in args:
		curDivs = unionLists(curDivs, i.getAllDivs())

	#For each value of their results:
	for v in curDivs:
		results = [rs.get(v, allDivs) if rs.contains(v) else Result.createEmpty() for rs in args]
		
		#Average them and add it to the fRes
		fRes.append(averageResults(*results))
	
	return ResultsSet(fRes)



#Stupid debugging functions
def showRes(r: Result):
	r.toPercentages().removedAbs().display()
def showRess(rs: ResultsSet, d: str):
	rs.get(d).toPercentages().display()