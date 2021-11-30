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
            if p.getFullName() == cand or p.getShortName() == cand: return True
        for c in self.listOfCandidates:
            if c.getFullName() == cand: return True
        return False

    def getShadeColor(self, cand: str, inParty: bool = False) -> Color:
        for p in self.listOfParties:
            if cand == p.getFullName() or cand == p.getShortName():
                return p.getShadeColor()
        for c in self.listOfCandidates:
            if cand == c.getFullName():
                if inParty: return c.getShadeColorInParty()
                else: return c.getShadeColor()
        
    def get(self, cand: str) -> Party|Candidate:
        for p in self.listOfParties:
            if cand == p.getFullName() or cand == p.getShortName():
                return p
        for c in self.listOfCandidates:
            if cand == c.getFullName():
                return c
    
    def getCircleColor(self, cand: str) -> Color:
        for p in self.listOfParties:
            if cand == p.getFullName() or cand == p.getShortName():
                return p.getCircleColor()
    
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
            listOfParties = [Party(x['fullName'], x['shortName'], x['abbr'], Color(x['circleColor']), Color(x['shadeColor']) if 'shadeColor' in x else Color(x['circleColor'])) for x in fd]
    
    if srcCandidates != '':
        with open(srcCandidates, 'r', encoding='utf8') as csvData:
            formattedData = [[y for y in x.split(';')] for x in csvData.read().split('\n')]
            fd = [{formattedData[0][i]: x[i] for i in range(len(x))} for x in formattedData[1:]]
            listOfCandidates = [Candidate(x['firstName'], x['lastName'], [p for p in listOfParties if (p.getFullName() == x['party'] or p.getShortName() == x['party'])][0], Color(x['shadeColor']), Color(x['shadeColorInParty'])) for x in fd]
    
    return Candidacies(listOfParties=listOfParties, listOfCandidates=listOfCandidates)
