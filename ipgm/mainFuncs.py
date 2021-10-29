from ipgm.Result import *
from ipgm.ResultsSet import *
from ipgm.ResultPerc import *
from ipgm.VTM import *

#Fonction pour extrapoler les résultats selon un autre ensemble de votes (peut être 1er tour 2017, 2nd tour 2017, ou premier tour de l'élection)
#Function to extrapolate ResultsSet
def extrapolateResults(initialRes: ResultsSet, changeMatrix: VTMatrix) -> ResultsSet:
	finalRes = []

	#for every line in the results:
	for res in initialRes.listOfResults:
		finalRes.append(extrapolateResult(res, changeMatrix))

	return ResultsSet(finalRes)

#Function to extrapolate single Result
def extrapolateResult(initialRes: Result, changeMatrix: VTMatrix) -> Result:
	allSumProducts = {cf: sumProductDict(initialRes.results, changeMatrix.getColDict(cf)) for cf in changeMatrix.final}
	allSumProducts = multiplyDict(allSumProducts, (initialRes.getSumOfVotes()/sumDict(allSumProducts)))
	return Result.fromLists(initialRes.name, list(allSumProducts.keys()), list(allSumProducts.values()))

#Fonction pour redresser les résultats par division (ou nationalement, si une seule division est donnée)
def redressementResults(initialRes: ResultsSet, targetRes: ResultPerc, allDivs: AllDivs):
	fRes = []
	
	#Get all components
	targetName = targetRes.name
	targetDivisions: list[str] = unpackDivisions(targetName, allDivs.firstLevel, allDivs.overLevel)
	
	#Compute the difference between the actual and target results
	actualRes: ResultPerc = initialRes.sumIfs(targetDivisions).toPercentages(newName=targetName)
	diff: dict[str, float] = targetRes.getSubstracted(actualRes)

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


#Fonction pour faire la moyenne de plusieurs redressements (par exemple, faire la moyenne de résultats extrapolés après le 1er tour 2017 et après le 1er tour 2022)
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

#Stupid debugging function
def showRes(r: Result, doReweight: bool = True):
	r.toPercentages(doReweight).removedAbs().display()
def showRess(rs: ResultsSet, d: str):
	rs.get(d).toPercentages().display()