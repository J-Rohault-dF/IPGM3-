from __future__ import annotations
from Result import *




class Div:
	superset: Div|None
	subset: list[Div]
	name: str
	result: Result

	def __init__(self, superset: Div|None, subset: list[Div] = [], name: str = '', result: Result|None = None):
		self.superset = superset
		self.subset = subset
		self.name = name
		self.result = result
	
	def contains(self, name: str) -> bool:
		if self.name == name: return True
		else:
			for i in self.subset:
				if i.contains(name): return True
			return False
	
	#Returns component given its name
	def get(self, name: str) -> Result:

		if self.name == name: return self
		else:
			for i in self.subset:
				ig = i.get(name)
				if ig != None: return ig
			return None
		#TODO: Check the auto-update (right now, a result isn't updated based on the results below)

	def insert(self, path: list[str], res: Result):
		
		if len(path) == 1:
			self.subset.append(Div(self, [], path[0], res))
		else:
			for sd in self.subset:
				if sd.name == path[0]:
					sd.insert(path[1:], res)
			else:
				sd = Div(self, [], path[0], Result())
				self.subset.append(sd)
				sd.insert(path[1:], res)