import typing
from colour import Color
from ipgm.Candidacy import Candidacy

Candidacies = typing.TypeVar('Candidacies')
class Candidacies:
	listOfCands: list[Candidacy] = []

	def __init__(self, listOfParties: list[Candidacy]):
		self.listOfCands = listOfParties
	
	def getAllCands(self, longNames: bool = False):
		return [c.getFullName() for c in self.listOfCands]

	def contains(self, cand: str) -> bool:
		for c in self.listOfCands:
			if cand == c.getFullName() or cand == c.getShortName(): return True
		return False

	def getShadeColor(self, cand: str) -> Color:
		for c in self.listOfCands:
			if cand == c.getFullName() or cand == c.getShortName():
				return c.getShadeColor()
		raise Exception(cand+': Candidacy not found')
		
	def get(self, cand: str) -> Candidacy:
		for c in self.listOfCands:
			if cand == c.getFullName() or cand == c.getShortName():
				return c
		raise Exception(f'Candidate {cand} not found')
	
	def getCircleColor(self, cand: str) -> Color:
		for c in self.listOfCands:
			if cand == c.getFullName() or cand == c.getShortName():
				return c.getCircleColor()
		raise Exception(f'No circle color for {cand}')



def importCandidacies(src: str = '') -> Candidacies:
	"""
	Imports the list of candidacies from a source file.
	"""
	listOfCands = []

	with open(src, 'r', encoding='utf8') as csvData:
		formattedData = [[y for y in x.split(';')] for x in csvData.read().split('\n')]
		fd = [{formattedData[0][i]: x[i] for i in range(len(x))} for x in formattedData[1:]]
		listOfCands = [Candidacy(fullName=x['fullName'], shortName=x['shortName'], circleColor=Color(x['circleColor']), shadeColor=Color(x['shadeColor']) if 'shadeColor' in x else Color(x['circleColor']), emoji=x['emoji']) for x in fd]
	
	return Candidacies(listOfCands)
