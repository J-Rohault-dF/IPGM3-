from ipgm.Party import *
from ipgm.Candidate import *

class Candidacies:
	listOfParties: list[Party] = []
	listOfCandidates: list[Candidate] = []

	def __init__(self, listOfParties: list[Party], listOfCandidates: list[Candidate]):
		self.listOfParties = listOfParties
		self.listOfCandidates = listOfCandidates
	
	def getAllCandidates(self, longNames: bool = False):
		return [c.getFullName() for c in self.listOfCandidates]

	def getAllParties(self, longNames: bool = False):
		return [(p.getFullName() if longNames else p.getShortName()) for p in self.listOfParties]
	
	def getAllCands(self, longNames: bool = False):
		return self.getAllCandidates()+self.getAllParties()
	
	def contains(self, cand: str) -> bool:
		for p in self.listOfParties:
			if cand in [p.getFullName(), p.getShortName(), p.getAbbr()]: return True
		for c in self.listOfCandidates:
			if c.getFullName() == cand: return True
		return False

	def getShadeColor(self, cand: str, inParty: bool = False) -> Color:
		for p in self.listOfParties:
			if cand in [p.getFullName(), p.getShortName(), p.getAbbr()]:
				return p.getShadeColor()
		for c in self.listOfCandidates:
			if cand == c.getFullName():
				if inParty: return c.getShadeColorInParty()
				else: return c.getShadeColor()
		
	def get(self, cand: str) -> Party|Candidate:
		for p in self.listOfParties:
			if cand in [p.getFullName(), p.getShortName(), p.getAbbr()]:
				return p
		for c in self.listOfCandidates:
			if cand == c.getFullName():
				return c
	
	def getCircleColor(self, cand: str) -> Color:
		for p in self.listOfParties:
			if cand in [p.getFullName(), p.getShortName(), p.getAbbr()]:
				return p.getCircleColor()
		for c in self.listOfCandidates:
			if cand == c.getFullName():
				return c.getCircleColor()
	
	def getPartyFromCandName(self, cand: str) -> Party:
		for c in self.listOfCandidates:
			if cand == c.getFullName():
				return c.getParty()



def importCandidacies(srcParties: str = '', srcCandidates: str = '') -> Candidacies:
	listOfParties = []
	listOfCandidates = []

	if srcParties != '':
		with open(srcParties, 'r', encoding='utf8') as csvData:
			formattedData = [[y for y in x.split(';')] for x in csvData.read().split('\n')]
			fd = [{formattedData[0][i]: x[i] for i in range(len(x))} for x in formattedData[1:]]
			listOfParties = [Party(fullName=x['fullName'], shortName=x['shortName'], abbr=x['abbr'], circleColor=Color(x['circleColor']), shadeColor=Color(x['shadeColor']) if 'shadeColor' in x else Color(x['circleColor']), emoji=x['emoji']) for x in fd]
	
	if srcCandidates != '':
		with open(srcCandidates, 'r', encoding='utf8') as csvData:
			formattedData = [[y for y in x.split(';')] for x in csvData.read().split('\n')]
			fd = [{formattedData[0][i]: x[i] for i in range(len(x))} for x in formattedData[1:]]
			listOfCandidates = [Candidate(firstName=x['firstName'], lastName=x['lastName'], party=extractParty(x, listOfParties), shadeColor=Color(x['shadeColor']), shadeColorInParty=Color(x['shadeColorInParty']), emoji=x['emoji']) for x in fd]
	
	return Candidacies(listOfParties=listOfParties, listOfCandidates=listOfCandidates)

def extractParty(x: dict[str, str], listOfParties: list[Party]):
	party = [p for p in listOfParties if (x['party'] in [p.getFullName(), p.getShortName(), p.getAbbr()])]
	if len(party) > 0: return party[0]
	else: return None
