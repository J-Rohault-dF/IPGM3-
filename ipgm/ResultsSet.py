from collectivites import *
from ipgm.Result import *

#Set of multiple results
class ResultsSet:
	listOfResults: list[Result] = []

	def __init__(self, listOfResults: list=[]):
		self.listOfResults = listOfResults
	
	def contains(self, name: str) -> bool:
		return name in [x.name for x in self.listOfResults]

	#Returns component given its name
	def get(self, name: str, allDivs: AllDivs, quiet: bool = False) -> Result:

		if name in [x.name for x in self.listOfResults]:
			return [x for x in self.listOfResults if x.name == name][0] #Dumb stupid code but I guess it maybe works
		
		elif name in list(allDivs.overLevel.keys()):
			cols = allDivs.overLevel[name]
			running = Result.fromDict(name, {})
			for r in [self.get(x, allDivs=allDivs) for x in cols]:
				running = running.add(r)
			return running
		else:
			if quiet: return None
			else: raise Exception('Subdivision {0} not found'.format(name))

	#Returns list of all components
	def getAll(self, listNames: list) -> list:
		return [self.get(x) for x in listNames]
	
	#Returns names of all components
	def getAllDivs(self) -> list:
		return [x.name for x in self.listOfResults]
	
	#Returns sum of all components if they are in the given list
	def sumIfs(self, conditionList: list) -> Result:
		running = Result.createEmpty()

		for r in self.listOfResults:
			if r.name in conditionList: running = running.add(r)

		return running
	
	def getSumIf(self, condition: str, allDivs: list, unpackingDivs: dict) -> dict:
		return self.sumIfs(unpackDivisions(condition, allDivs, unpackingDivs))

	def getSumAll(self, allDivs: AllDivs) -> dict:
		return self.getSumIf('National', allDivs.firstLevel, allDivs.overLevel)