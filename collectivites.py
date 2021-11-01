from ipgm.utils import *

class AllDivs:
	firstLevel = []
	overLevel = {}
	allDivs = []

	def __init__(self, src: str):
		with open(src, 'r', encoding='utf8') as divs:
			allFirstLines = [line.strip() for line in divs if (line.strip() != '' and ':' not in line)]
			divs.seek(0)
			allOverLines = {line.split(':')[0].strip(): [x.strip() for x in line.split(':')[1].split(';')] for line in divs if ':' in line}
		
		self.firstLevel = allFirstLines
		self.overLevel = allOverLines
		self.allDivs = getSetList(allFirstLines + list(allOverLines.keys()))

	def getSortingKeys(self, s: str):
		return self.allDivs.index(s)