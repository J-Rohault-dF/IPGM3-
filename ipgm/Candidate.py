from ipgm.Party import *
from colour import *

class Candidate:
	firstName: str
	lastName: str
	fullName: str
	party: Party
	shadeColor: Color
	shadeColorInParty: Color
	emoji: str

	def __init__(self, firstName: str, lastName: str, party: Party, shadeColor: Color, shadeColorInParty: Color, reverseName: bool = False, emoji: str = None):
		self.firstName = firstName
		self.lastName = lastName
		self.fullName = firstName+' '+lastName if not reverseName else lastName+' '+firstName
		self.party = party
		self.shadeColor = shadeColor if (shadeColor != Color('') and shadeColor != None) else self.party.getShadeColor()
		self.shadeColorInParty = shadeColorInParty if (shadeColorInParty != Color('') and shadeColorInParty != None) else party.getShadeColor() if party != None else Color('')
		self.emoji = emoji if emoji != '' else None

	def __repr__(self):
		return '<Candidate: {fullName} ({partyName}), shadeColor {shadeColor} ({inParty} in party)>'.format(fullName=self.fullName, partyName=self.party.getShortName(), shadeColor=self.shadeColor, inParty=self.shadeColorInParty)

	#Getters
	def getFirstName(self) -> str: return self.firstName
	def getLastName(self) -> str: return self.lastName
	def getFullName(self) -> str: return self.fullName
	def getParty(self) -> Party: return self.party
	def getShadeColor(self) -> Color: return self.shadeColor
	def getShadeColorInParty(self) -> Color: return self.shadeColorInParty
	def getEmoji(self) -> str: return self.party.getEmoji() if self.emoji == None else self.emoji
	def getCircleColor(self) -> Color: return self.party.getCircleColor() if self.party != None else self.shadeColor
