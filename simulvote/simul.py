from __future__ import annotations
from ipgm.Result import *
from ipgm.Div import *
import random
import math
import copy
import time

from ipgm.mainFuncs import redressementResults

def simulOneRes(res: Result, stdev: float, sampleSize: int) -> Result:
	totalVotes = res.getSumOfVotes()
	rr = {}
	for k,v in res.results.items():
		if not isExpressed(k): continue
		p = v/totalVotes
		rr[k] = random.gauss(p, stdev*math.sqrt(p*(1-p) / sampleSize))
	return Result({k: v*totalVotes for k,v in rr.items()})



def rankingChances(res: Result, amountOfSims: int, stdev: float, sampleSize: int, top: int) -> dict[str, float]:
	#Do N times:
	allCands = [x for x in res.getCandidates() if isCandidate(x)]

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



def simulOneNat(odiv: Div, stdev: float, sampleSize: int) -> Div:
	div = copy.deepcopy(odiv)

	#Generate national swing
	nat = simulOneRes(div.result, stdev, sampleSize)

	#Generate swing for all depts
	for sd in div.allBaseSubDivs():
		sd.result = simulOneRes(sd.result, stdev, sampleSize)

	#Redresse all depts according to the national swinged result
	div.recalculateAll()
	div = redressementResults(div, nat.toPercentages(div.name))

	#return new rs
	return div



def simulMany(div: Div, amountOfSims: int, stdev: float, sampleSize: int, listSim: list[str] = None) -> dict:
	timeStart = time.time()
	
	if listSim == None: listSim = [x.name for x in div.allBaseSubDivs()]
	ls = {k: {} for k in listSim}

	candidates = [x for x in div.result.getCandidates() if isExpressed(x)]

	div = simplifyDivTree(div, threshold=0.125)

	print('Initialized… {0}'.format(time.time()-timeStart))

	#Do many times:
	for i in range(amountOfSims):

		# Simulate one election
		dt = simulOneNat(div, stdev, sampleSize)
		#dt = simplifyDivTree(dt)

		# Find the winners in each dept and put them in some array
		for d in listSim:
			w = dt.get(d).result.getWinner()
			addInDict(ls[d], w, 1)
			#if w in ls[d]: ls[d][w] += 1
			#else: ls[d][w] = 1
		
		if i%(amountOfSims/10) == 0:
			print('Simulated {0} out of {1}… {2}s'.format(i, amountOfSims, round(time.time()-timeStart, 1)))
		
	# Count how many times each candidate is in an array and find how safe the dept is
	lDepts = {}

	for k,v in ls.items():
		lDepts[k] = {x: v[x]/sum(v.values()) if (x in v) else 0 for x in candidates}

	# Return the results
	return lDepts

def simplifyDivTree(div: Div, threshold: float = 0.1) -> Div: #Removes all candidates below the threshold, changes the object and returns it
	for d in div.allBaseSubDivs():

		r = d.result
		rp = r.toPercentages()
		maxScore = rp.get(r.getWinner())

		dc = {'@': 0} #TODO: Instead of passing through resultsperc, calculate the threshold in votes then check directly
		for k,v in rp.results.items():
			if v >= (maxScore-threshold):
				dc[k] = v
			else:
				dc['@'] += v
		
		d.result = Result.fromPercentages(ResultPerc.fromVotelessDict(d.name, dc, r.getSumOfVotes(removeAbs=False)))

	div.recalculateAll()
	return div