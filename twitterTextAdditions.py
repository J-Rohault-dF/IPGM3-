from ipgm.ResultsSet import *
from simulvote.simul import *
import math

#Both next functions should be given a national Result in argument

#Generate tweet text
def makeTweetText(natRes: ResultPerc, sampleSize: int, top: int) -> str:
	natRes = natRes.removedAbs()
	cands: list[str] = [k for k,v in sorted(natRes.results.items(), key=lambda x: x[1], reverse=True) if v+getMarginOfError(sampleSize, v, 1.96) >= 0.05]
	ranks = rankingChances(Result.fromPercentages(natRes), 5000, 1.96, sampleSize, top)
	
	allLines = []
	for c in cands:
		allLines.append('{e} {cand}: {sc} {q}'.format(e=getEmoji(c), cand=c, sc=formatScoreWithMargins(sampleSize, natRes.get(c), 1.96), q=getScoreClock(ranks[c])))
	return '\n'.join(allLines)

#Compute chances per candidate

#UTIL - Get color emojis for candidates
def getEmoji(cand: str) -> str:
	if cand in ['Jean-Luc Mélenchon', 'Nathalie Arthaud', 'Philippe Poutou', 'Fabien Roussel']:
		return '🟪' #EXG

	elif cand in ['Yannick Jadot', 'Antoine Waechter', 'Sandrine Rousseau', 'Delphine Batho', 'Éric Piolle', 'Jean-Marc Governatori']:
		return '🟩' #ÉCO

	elif cand in ['Anne Hidalgo', 'Arnaud Montebourg', 'Stéphane Le Foll', 'Gérard Filoche', 'Pierre Larrouturou']:
		return '🟥' #GAU

	elif cand in []:
		return '🟧' #RÉG

	elif cand in ['Emmanuel Macron', 'Jean-Christophe Lagarde']:
		return '🟨' #CEN

	elif cand in ['Xavier Bertrand', 'Valérie Pécresse', 'Michel Barnier', 'Éric Ciotti', 'Philippe Juvin', 'Denis Payre', 'Jean Lassalle', 'Jean-Frédéric Poisson']:
		return '🟦' #DRT

	elif cand in ['Marine Le Pen', 'Éric Zemmour', 'François Asselineau', 'Nicolas Dupont-Aignan', 'Florian Philippot']:
		return '🟫' #EXD

	elif cand in []:
		return '⬛' #?

	else:
		return '⬜' #AUT

def formatScoreWithMargins(sampleSize: int, score: float, sigma: float) -> str:
	moe = getMarginOfError(sampleSize, score, sigma)
	return '{0}~{1}%'.format(round((score-moe)*100), round((score+moe)*100))

def getMarginOfError(sampleSize: int, score: float, sigma: float) -> float:
	return sigma * math.sqrt(score*(1-score) / sampleSize)

def getScoreClock(score: float) -> str:
	return ['','🕐','🕑','🕒','🕓','🕔','🕕','🕖','🕗','🕘','🕙','🕚','🕛'][round(score*12)]