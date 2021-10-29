from ipgm.Result import *
from ipgm.ResultsSet import *
import random
import math
import copy

from ipgm.mainFuncs import redressementResults

def simulOneRes(res: Result, stdev: float, sampleSize: int) -> Result:
	rp = res.toPercentages()
	rr = copy.deepcopy(rp)
	for i in rp.getCandidates():
		p = rr.results[i]
		rr.results[i] = random.gauss(rr.results[i], stdev*math.sqrt(p*(1-p) / sampleSize))
	return Result.fromPercentages(rr.removedAbs())



def rankingChances(res: Result, amountOfSims: int, stdev: float, sampleSize: int, top: int) -> dict[str, float]:
	#Do N times:
	allCands = [x for x in res.getCandidates() if x != '@']

	ls = {c: 0 for c in allCands}

	for i in range(amountOfSims):
		# Simul 1 national result
		n = simulOneRes(res, stdev, sampleSize)
		# Store the rank of each candidate
		for c in allCands:
			if getRankInDict(n.results, c) < top:
				ls[c] += 1
	
	#Return the chances for each candidate to get some rann
	return {k: v/amountOfSims for k,v in ls.items()}



def simulOneNat(ress: ResultsSet, stdev: float, sampleSize: int, allDivs: AllDivs) -> ResultsSet:
	#Generate national swing
	nat = Result.fromPercentages(simulOneRes(ress.get('National', allDivs=allDivs), stdev, sampleSize))

	#Generate swing for all depts
	for r in ress.listOfResults:
		r = Result.fromPercentages(simulOneRes(r, stdev, sampleSize))

	#Redresse all depts according to the national swinged result
	ress = redressementResults(ress, nat, allDivs=allDivs)

	#return new rs
	return ress



def simulMany(ress: ResultsSet, amountOfSims: int, stdev: float, sampleSize: int, allDivs: AllDivs):
	
	ls = dict(zip( allDivs.allDivs, [ {} for _ in range(len(allDivs.allDivs))]))

	candidates = [x for x in ress.get('National', allDivs).getCandidates() if x != '@']

	#Do many times:
	for i in range(amountOfSims):

		# Simulate one election
		rs = simulOneNat(ress, stdev, sampleSize, allDivs)

		# Find the winners in each dept and put them in some array
		for d in allDivs.allDivs:
			w = rs.get(d, allDivs).getWinner()
			if w in ls[d]: ls[d][w] += 1
			else: ls[d][w] = 1
		
		if i%(amountOfSims/5) == 0:
			print('Simulated {0} out of {1}...'.format(i, amountOfSims))
		
	# Count how many times each candidate is in an array and find how safe the dept is
	lDepts = {}

	for k,v in ls.items():
		lDepts[k] = {x: v[x]/sum(v.values()) if (x in v) else 0 for x in candidates}

	# Return the results
	return lDepts