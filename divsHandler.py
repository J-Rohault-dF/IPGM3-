from __future__ import annotations
from ipgm.utils import *

class AllDivs:
	firstLevel = []
	overLevel = {}
	allDivs = []

	def __init__(self, src: str, ignore: str = []):
		with open(src, 'r', encoding='utf8') as divs:
			allFirstLines = [line.strip() for line in divs if (line.strip() != '' and ':' not in line and line.strip() not in ignore)]
			divs.seek(0)
			allOverLines = {line.split(':')[0].strip(): [x.strip() for x in line.split(':')[1].split(';')] for line in divs if ':' in line}
		
		for i in ignore: #Handles ignored divs
			for j in allOverLines[i]:
				allFirstLines.remove(j)
			del allOverLines[i]
			allFirstLines.append(i)
		
		self.firstLevel = allFirstLines
		self.overLevel = allOverLines
		self.allDivs = getSetList(allFirstLines + list(allOverLines.keys()))

	def getSortingKeys(self, s: str):
		return self.allDivs.index(s)
	
	def under(self, div):
		return self.overLevel[div]
	
	def unders(self, div):
		if div in self.firstLevel: return div
		else:
			return flattenList([self.unders(x) for x in self.under(div)])
	
	def getPath(self, div: str) -> list[str]:
		path = [div]

		for k,v in self.overLevel:
			if v == div:
				path = self.getPath(k)
				path.append(k)

		return path