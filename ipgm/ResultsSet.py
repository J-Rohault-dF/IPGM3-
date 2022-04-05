from __future__ import annotations
from divsHandler import *
from ipgm.Result import *

#Set of multiple results
class ResultsSet:
	headResult: Result
	allDivs: AllDivs

	#def __init__(self, allDivs: AllDivs, listOfResults: list=[]):
	#	self.listOfResults = listOfResults
	#	self.allDivs = allDivs
	
	def __init__(self, allDivs: AllDivs, headResult: Result = Result()):
		self.headResult = headResult
		self.allDivs = allDivs

	def contains(self, name: str) -> bool:
		return self.headResult.contains(name)
	
	def exportDict(self):
		return self.headResult.exportDict()

	#Returns component given its name
	def get(self, name: str, quiet: bool = False) -> Result:
		res = self.headResult.get(name)
		if res == None and not quiet: raise Exception('Subdivision {0} not found'.format(name))
		else: return res
	
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
		self.headResult.subset = newList

	def replaceCand(self, div: str, cand: str, replacing: str):
		for i in self.allDivs.unders(div):
			self.set(self.get(i).replaceCand(cand, replacing))