from colour import *

class Candidacy:
	fullName: str
	shortName: str
	circleColor: Color
	shadeColor: Color
	emoji: str

	def __init__(self, fullName: str, shortName: str, circleColor: Color, shadeColor: Color, emoji: str):
		self.fullName = fullName
		self.shortName = shortName
		self.circleColor = circleColor
		self.shadeColor = shadeColor
		self.emoji = emoji
	
	def __repr__(self):
		return '<Candidacy: {fullName} ({shortName}), circleColor {circleColor}, shadeColor {shadeColor} ({emoji})>'.format(fullName=self.fullName, shortName=self.shortName, circleColor=self.circleColor, shadeColor=self.shadeColor, emoji=self.emoji)
	
	#Getters
	def getFullName(self) -> str: return self.fullName
	def getShortName(self) -> str: return self.shortName
	def getCircleColor(self) -> Color: return self.circleColor
	def getShadeColor(self) -> Color: return self.shadeColor
	def getEmoji(self) -> str: return self.emoji
