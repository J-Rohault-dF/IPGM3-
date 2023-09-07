from __future__ import annotations
from typing import Dict
from ipgm.utils import *

class ResultPerc:
	name: str = ''
	results: dict[str, float] = {}
	totalVotes: float|None = None

	def __init__(self, name: str, resDict: dict[str, float], totalVotes: float|None):
		self.name = name
		self.results = {k: v/sum(resDict.values()) for k,v in resDict.items()}
		self.totalVotes = totalVotes
	
	@classmethod
	def fromVotesDict(self, name: str, resDict: Dict):
		return ResultPerc(name, resDict, sum([x for x in resDict.values()]))
	
	@classmethod
	def fromVotelessDict(self, name: str, resDict: dict, votesCount: int|float|None = None):
		return ResultPerc(name, resDict, votesCount)
	
	@classmethod
	def createEmpty(self):
		return ResultPerc('', {}, None)

	def __repr__(self):
		return '<{0}: {1} votes, {2}>'.format(self.name, self.totalVotes, self.results)

	

	def get(self, cand: str) -> float:
		if self.hasCandidate(cand):
			return self.results[cand]
		else:
			raise Exception('Requested candidate {0} not in {1}'.format(cand, self))

	def getCandidates(self) -> list[str]:
		return [x for x in self.results.keys()]
		
	def getSumOfVotes(self) -> float:
		return self.totalVotes
	
	def hasCandidate(self, cand: str) -> bool:
		return cand in self.results.keys()



	def getAdded(self, other: ResultPerc) -> ResultPerc:
		allKeys = unionLists(self.getCandidates(), other.getCandidates())
		finalRes = {}
		for k in allKeys:
			finalRes[k] = ( self.results[k] if self.hasCandidate(k) else 0 ) + ( other.results[k] if other.hasCandidate(k) else 0 )
		
		votes = (self.totalVotes if self.totalVotes != None else 0) + (other.totalVotes if other.totalVotes != None else 0)
		return ResultPerc(self.name, finalRes, votes)

	def getAddedDict(self, other: dict[str, float]) -> ResultPerc:
		allKeys = unionLists(self.getCandidates(), other)
		finalRes = {}
		for k in allKeys:
			finalRes[k] = ( self.results[k] if self.hasCandidate(k) else 0 ) + ( other[k] if k in other.keys() else 0 )
		
		return ResultPerc(self.name, finalRes, self.totalVotes)

	def getMultipliedDict(self, other: dict[str, float], doReweight: bool = False) -> ResultPerc:
		allKeys = unionLists(self.getCandidates(), other)
		finalRes = {}
		for k in allKeys:
			finalRes[k] = ( self.results[k] if self.hasCandidate(k) else 0 ) * ( other[k] if k in other.keys() else 0 )
		
		if doReweight: return ResultPerc(self.name, percentDict(finalRes), self.totalVotes)
		else: return ResultPerc(self.name, percentDict(finalRes), self.totalVotes*mean(finalRes))

	def getSubstracted(self, other: ResultPerc) -> dict[str, float]:
		allKeys = unionLists(self.getCandidates(), other.getCandidates())
		finalRes = {}

		for k in allKeys:
			finalRes[k] = ( self.results[k] if k in self.getCandidates() else 0 ) - ( other.results[k] if k in other.getCandidates() else 0 )
		
		return finalRes

	def getDivided(self, other: ResultPerc) -> dict[str, float]:
		allKeys = unionLists(self.getCandidates(), other.getCandidates())
		finalRes = {}

		for k in allKeys:
			finalRes[k] = ( self.results[k] if k in self.getCandidates() else 0 ) / ( other.results[k] if k in other.getCandidates() else 1 )
		
		return finalRes
	
	def getReadjusted(self):
		return {k: v/sum(self.results.values()) for k,v in self.results.items()}

	def display(self):
		print('{0}: {1} total votes - '.format(self.name, self.totalVotes) + ', '.join(['{0}: {1}'.format(x, formatPerc(self.results[x])) for x in sorted(self.results, key=self.results.__getitem__, reverse=True)]))
	
	def removedAbs(self):
		if hasNonExpressed(self.results): return ResultPerc(self.name, {k:v for k,v in self.results.items() if isExpressed(k)}, self.totalVotes*(1-nonExpressed(self.results)))
		else: return self
	
	def removedCand(self, cand: str):
		return ResultPerc(self.name, {k:v for k,v in self.results.items() if k != cand}, self.totalVotes*(1-self.get(cand)))

	def zipZeroes(self):
		self.results = {k: max(v,0) for k,v in self.results.items()}