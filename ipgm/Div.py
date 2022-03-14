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
		return '<{0}: {1}, contains {2}>'.format(self.name, self.result.results, [x.name for x in self.subset])
	
	def getTree(self):
		return {x.name: x.getTree() for x in self.subset}

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

	"""def insert(self, path: list[str], res: Result):
		print('')
		print('{0}.insert({1}, /), {2}'.format(self.name, path, self.getTree()))

		if len(path) == 1:
			print('len(path == 1)')
			self.subset.append(Div(self, [], path[0], res))
			#print(self)
		elif len(path) == 0:
			return None
		else:
			print('else:')
			print('searching in {0}'.format([x.name for x in self.subset]))
			for sd in self.subset:
				print('trying to find… {0}'.format(sd.name))
				if sd.name == path[0]:
					print('found it')
					sd.insert(path[1:], res)
					break
			else:
				print('didn\'t find it')
				nsd = Div(self, [], path[0], Result())
				self.subset.append(nsd)
				nsd.insert(path[1:], res)"""
	
	def exportDict(self):
		d = {}
		d[self.name] = self.result.results
		for x in self.subset:
			d = appendDict(d, x.exportDict)
		return d
	
	def recalculate(self):
		r = self.subset[0].result
		for i in self.subset[1:]:
			r.add(i.result)
		self.result = r
	
	def insert(self, sub: Div):
		print('inserting {0} in {1}'.format(sub.name, self.name))
		self.subset.append(sub)
		sub.superset.append(self)
