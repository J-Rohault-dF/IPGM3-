from simulvote.simul import *
import math

#Both next functions should be given a national Result in argument

#Generate tweet text
def makeTweetText(natRes: ResultPerc, sampleSize: int, top: int, nbSimulated: int, candidaciesData: Candidacies, threshold: float = 0) -> str:
	natRes = natRes.removedAbs()
	cands: list[str] = [k for k,v in sorted(natRes.results.items(), key=lambda x: x[1], reverse=True) if v+getMarginOfError(sampleSize, v, 1.96) >= threshold]
	ranks = rankingChances(Result.fromPercentages(natRes), nbSimulated, 1.96, sampleSize, top)
	
	allLines = []
	for c in cands:
		allLines.append('{e} {cand}: {sc}{q}'.format(e=candidaciesData.get(c).getEmoji(), cand=c, sc=formatScoreWithMargins(sampleSize, natRes.get(c), 1.96), q=getScoreClock(ranks[c])))
	return '\n'.join(allLines)

def formatScoreWithMargins(sampleSize: int, score: float, sigma: float) -> str:
	moe = getMarginOfError(sampleSize, score, sigma)
	return '{0}~{1}%'.format(round((score-moe)*100), round((score+moe)*100))

def getMarginOfError(sampleSize: int, score: float, sigma: float) -> float:
	return sigma * math.sqrt(score*(1-score) / sampleSize)

def getScoreClock(score: float) -> str:
	return ['',' 🕐',' 🕑',' 🕒',' 🕓',' 🕔',' 🕕',' 🕖',' 🕗',' 🕘',' 🕙',' 🕚',' 🕛'][round(score*12)]