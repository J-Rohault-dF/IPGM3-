
from ipgm.utils import *

class AllDivs:
	firstLevel = []
	overLevel = {}
	allDivs = []

	def __init__(self, src: str, ignore: str = []):
		with open(src, 'r', encoding='utf8') as divs:
			allFirstLines = [line.strip() for line in divs if (line.strip() != '' and ':' not in line and line.strip() not in ignore)]
			divs.seek(0)

			allOverLines = {}
			for line in divs:
				if ':' in line:
					divTitle = line.split(':')[0].strip()

					if divTitle not in allOverLines: #Add all subdivs
						allOverLines[divTitle] = []
					allOverLines[divTitle] += [x.strip() for x in line.split(':')[1].split(';')]
		
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
		path = []
		print('getting path for {0}'.format(div))

		for k,v in self.overLevel.items():
			if div in v:
				print('found {0} around {1}'.format(k, v))
				path = self.getPath(k)
				path.append(div)
				break
		else:
			print('added {0}'.format(div))
			path = [div]

		print('returns {0}'.format(path))
		return path
