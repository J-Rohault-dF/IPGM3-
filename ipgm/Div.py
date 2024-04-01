import typing
from ipgm.Result import *



Div = typing.TypeVar('Div')
class Div:
	superset: list[Div]
	subset: list[Div]
	name: str
	result: Result

	def __init__(self, superset: list[Div] = [], subset: list[Div] = [], name: str = '', result: Result = Result()):
		self.superset = superset
		self.subset = subset
		self.name = name
		self.result = result
	
	def __repr__(self):
		return '<{0}: {1}, contains {2}, part of {3}>'.format(self.name, (self.result.results if self.result is not None else 'None'), [x.name for x in self.subset], [x.name for x in self.superset])
	
	def getTree(self):
		return {x.name: x.getTree() for x in self.subset}

	def contains(self, name: str) -> bool:
		if self.name == name: return True
		else:
			for i in self.subset:
				if i.contains(name): return True
			return False
	
	#Returns component given its name
	def get(self, name: str) -> Div:

		gotten = self.__getRecursive(name)

		if gotten is None: raise Exception(f'Div {name} not found in {self.name}')

		return gotten

		#TODO: Check the auto-update (right now, a result isn't updated based on the results below)
	
	def __getRecursive(self, name: str) -> Div|None:
		if self.name == name:
			return self
		else:
			for i in self.subset:
				ig = i.__getRecursive(name)
				if ig is not None:
					return ig
			return None
	
	def exportDict(self):
		d = {}
		d[self.name] = self.result.results
		for x in self.subset:
			d = appendDict(d, x.exportDict())
		return d
	
	def recalculateAll(self): #Recursive recalculate() call in all subdivs
		if self.subset != []:
			self.recalculate()
			for d in self.subset:
				d.recalculateAll()
	
	def allBaseSubDivs(self) -> list[Div]: #Calculates recursively the list of all base subdivs
		if self.subset == []:
			return [self]
		ls = []
		for d in self.subset:
			ls = mergeSetLists(ls, d.allBaseSubDivs())
		return ls
	
	def allSubDivs(self) -> list: #Calculates recursively the list of all subdivs (not only base)
		ls = [self]
		for d in self.subset:
			ls = mergeSetLists(ls, d.allSubDivs())
		return ls

	def recalculate(self) -> None: #Calculate recursive sum of all subdivs under
		if self.subset == []:
			return None
		self.subset = sorted(self.subset, key=lambda x: x.name)
		ls = [d.result for d in self.allBaseSubDivs()]
		#Sum all res
		rz = ls.pop()
		for rr in ls:
			rz = rz.getAdded(rr)
		self.result = rz

	def insert(self, sub: Div):
		self.subset.append(sub)
		sub.superset.append(self)
	
	def clear(self):
		self.result = Result.createEmpty()
		for sd in self.subset:
			sd.clear()
		return self

	def renameCandidate(self, cand, renamedTo):
		for d in self.allBaseSubDivs():
			d.result.renameCandidate(cand, renamedTo)
		self.recalculateAll()
		return self
	
	def removeCandidate(self, cand):
		for d in self.allBaseSubDivs():
			d.result.removeCandidate(cand)
		self.recalculateAll()
		return self
	
	def selectCandidates(self, cands: list[str]):
		for d in self.allBaseSubDivs():
			d.result.selectCandidates(cands)
		self.recalculateAll()
		return self

	def mergeCandidates(self, cand, mergedInto):
		for d in self.allBaseSubDivs():
			d.result.mergeCandidates(cand, mergedInto)
		self.recalculateAll()
		return self
	
	def multiply(self, factor: float):
		for sd in self.allBaseSubDivs():
			if sd == self: continue
			sd.result.multiply(factor)
		self.recalculate()
	
	def coalition(self, coalObj: dict[str, list[str]]) -> Div:
		"""
		Merges candidates in coalitions
		coalObj must be in the form {'coal1': ['list1', 'list2'],…}
		"""
		for d in self.allBaseSubDivs():
			d.result.coalition(coalObj)
		self.recalculateAll()
		return self

	def maximumScore(self, party) -> float:
		currentMaximum: float = 0
		for sd in self.allBaseSubDivs():
			if sd == self: continue
			score = sd.maximumScore(party)
			if score > currentMaximum: currentMaximum = score
		
		if party in self.result.results:
			score = self.result.results[party] / self.result.getSumOfVotes()
			if score > currentMaximum: currentMaximum = score

		return currentMaximum



def averageDivs(divs: list[Div], superset: list[Div] = []) -> Div:
	if len(divs) == 1: return divs[0]
	
	if not allValuesEqual([x.name for x in divs]): raise Exception('Attempts averaging different levels: {0}'.format([x.name for x in divs]))

	#Get the list and average
	divA = copy.deepcopy(divs[0]).clear()
	for dn in [x.name for x in divA.allBaseSubDivs()]:
		divA.get(dn).result = averageResults([x.get(dn).result for x in divs])
	
	divA.recalculateAll()
	return divA