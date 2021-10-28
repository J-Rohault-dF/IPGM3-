from ipgm.utils import *

def getFirstLevelDivs(src: str) -> list[str]:
	with open(src, 'r', encoding='utf8') as divs:
		allLines = [line.strip() for line in divs if (line.strip() != '' and ':' not in line)]
	return allLines

def getOverLevelDivs(src: str) -> dict[str, list[str]]:
	with open(src, 'r', encoding='utf8') as divs:
		allLines = {line.split(':')[0].strip(): [x.strip() for x in line.split(':')[1].split(';')] for line in divs if ':' in line}
	return allLines

class AllDivs:
	firstLevel = []
	overLevel = {}
	allDivs = []

	def __init__(self, src: str):
		self.firstLevel = getFirstLevelDivs(src)
		self.overLevel = getOverLevelDivs(src)
		self.allDivs = getSetList(self.firstLevel + list(self.overLevel.keys()))