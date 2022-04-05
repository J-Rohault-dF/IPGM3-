from __future__ import annotations
from copy import deepcopy
from ipgm.ResultPerc import *
from ipgm.utils import *
from ipgm.Candidacies import *

#Single line of results
class Result:
	results = {}

	def __init__(self, results: dict = {}):
		self.results = results

	@classmethod
	def fromLists(self, candidates: list, results: list):
		return Result(dict(zip(candidates, [toFloat(x) for x in results])))

	@classmethod
	def fromDict(self, results: dict):
		return Result(results)
	
	@classmethod
	def createEmpty(self):
		return Result('', {})

	def __repr__(self):
		return '<Results {0}>'.format(self.results)
	
	def getSumOfVotes(self, removeAbs: bool = True) -> float: #SHOULD REMOVE PARAMETER removeAbs
		if removeAbs:
			return sum([v for k,v in self.results.items() if k != '@'])
		else:
			return sumDict(self.results)
	
	def getCandidates(self) -> list[str]:
		return list(self.results.keys())

	def getAdded(self, other: Result):
		allCands = unionLists(self.getCandidates(), other.getCandidates())
		newRes = {}
		for c in allCands:
			newRes[c] = ( self.results[c] if c in self.getCandidates() else 0 ) + ( other.results[c] if c in other.getCandidates() else 0 )

		return Result.fromDict(newRes)

	def add(self, other: Result) -> Result:
		self = self.getAdded(other)
		return self
	
	def toPercentages(self, newName: str = '') -> ResultPerc:
		return ResultPerc.fromVotesDict(newName, self.results)
	
	@classmethod
	def fromPercentages(self, percs: ResultPerc):
		return Result(percs.name, {k: v*percs.totalVotes for k,v in percs.results.items()})
	
	def hasCandidate(self, cand: str) -> bool:
		return cand in self.getCandidates()
	
	def getWinner(self) -> str:
		s = ('', 0)
		for k,v in self.results.items():
			if v > s[1] and k != '@':
				s = (k, v)
		return s[0]
	
	def getCleanResults(self) -> dict[str, int|float]:
		return {k: v for k,v in self.results.items() if ('@' not in k and k != '')}

	def replaceCand(self, cand, replacing):
		self.results[replacing] = self.results.pop(cand)
		return self
	
	def checkEqualParty(self, candidaciesData: Candidacies) -> bool:

		toCheck = [x for x in self.results.keys() if x in candidaciesData.getAllCandidates()]
		if len(toCheck) == 0: return False

		firstParty = candidaciesData.getPartyFromCandName(toCheck[0]).getFullName()

		for c in toCheck[1:]:
			if candidaciesData.getPartyFromCandName(c).getFullName() != firstParty: return False
		return True
	
	def sortByVotes(self, doRandom: bool = False):
		import random
		ks = list(self.results.keys())
		if doRandom:
			random.shuffle(ks)
			self.results = {k: self.results[k] for k in ks}
		self.results = {k: v for k,v in sorted(self.results.items(), key=lambda x: x[1], reverse=True)}




def averageResults(*args: Result) -> Result:
	
	allCands = []
	for r in args:
		allCands = unionLists(allCands, r.getCandidates())
	fRes = {}
	percentages = [r.toPercentages() for r in args]

	for c in allCands:
		fRes[c] = averageList([p.get(c) if p.hasCandidate(c) else 0 for p in percentages])

	if allEquals([x.name for x in args]): fName = args[0].name
	elif len([x.name for x in args if x.name != '']) == 1: fName = [x.name for x in args if x.name != ''][0]
	else: fName = 'Average of {0}'.format(getSetList([x.name for x in args]).__str__())

	return Result.fromPercentages(ResultPerc(fName, fRes, averageList([x.totalVotes for x in percentages])))