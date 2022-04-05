from __future__ import annotations
from ipgm.Result import *




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
		return '<{0}: {1}, contains {2}, part of {3}>'.format(self.name, (self.result.results if self.result != None else 'None'), [x.name for x in self.subset], [x.name for x in self.superset])
	
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

		if self.name == name:
			return self
		else:
			for i in self.subset:
				ig = i.get(name)
				if ig != None:
					return ig
			return None
		#TODO: Check the auto-update (right now, a result isn't updated based on the results below)
	
	def exportDict(self):
		d = {}
		d[self.name] = self.result.results
		for x in self.subset:
			d = appendDict(d, x.exportDict)
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
	
	def allSubDivs(self) -> list[Div]: #Calculates recursively the list of all subdivs (not only base)
		ls = [self]
		for d in self.subset:
			ls = mergeSetLists(ls, d.allSubDivs())
		return ls

	def recalculate(self) -> None: #Calculate recursive sum of all subdivs under
		if self.subset == []:
			return None
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
		self.result = None
		for sd in self.subset:
			sd.clear()
		return self



def averageDivs(divs: list[Div], superset: list[Div] = []) -> Div:
	if len(divs) == 1: return divs[0]
	
	if not allValuesEqual([x.name for x in divs]): raise Exception('Attemps averaging different levels: {0}'.format([x.name for x in divs]))

	#Get the list and average
	divA = copy.deepcopy(divs[0]).clear()
	for dn in [x.name for x in divA.allBaseSubDivs()]:
		divA.get(dn).result = averageResults([x.get(dn).result for x in divs])
	
	divA.recalculateAll()
	return divA