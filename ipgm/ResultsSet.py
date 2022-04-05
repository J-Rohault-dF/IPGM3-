from __future__ import annotations
from divsHandler import *
from ipgm.Result import *

#Set of multiple results
class ResultsSet:
	listOfResults: list[Result] = []
	allDivs: AllDivs

	def __init__(self, allDivs: AllDivs, listOfResults: list=[]):
		self.listOfResults = listOfResults
		self.allDivs = allDivs
	
	def contains(self, name: str) -> bool:
		return name in [x.name for x in self.listOfResults]
	
	def exportDict(self):
		d = {}
		for x in self.listOfResults:
			d[x.name] = x.results
		return d

	#Returns component given its name
	def get(self, name: str, quiet: bool = False) -> Result:

		if name in [x.name for x in self.listOfResults]:
			return [x for x in self.listOfResults if x.name == name][0] #Dumb stupid code but I guess it maybe works
		
		elif name in list(self.allDivs.overLevel.keys()):
			cols = self.allDivs.overLevel[name]
			running = Result.fromDict(name, {})
			for r in [self.get(x) for x in cols]:
				running = running.add(r)
			return running
		else:
			if quiet: return None
			else: raise Exception('Subdivision {0} not found'.format(name))
	
	def set(self, res: Result):
		if res.name not in [x.name for x in self.listOfResults]:
			self.listOfResults.append(res)
		else:
			self.listOfResults[[x.name for x in self.listOfResults].index(res.name)] = res

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
	
	def getSumIf(self, condition: str, unpackingDivs: dict) -> dict:
		return self.sumIfs(unpackDivisions(condition, unpackingDivs))

	def getSumAll(self) -> dict:
		return self.getSumIf('National', self.allDivs.firstLevel, self.allDivs.overLevel)

	def trim(self, ls: list) -> None:
		newList = [self.get(x) for x in ls]
		self.listOfResults = newList

	def replaceCand(self, div: str, cand: str, replacing: str):
		for i in self.allDivs.unders(div):
			self.set(self.get(i).replaceCand(cand, replacing))