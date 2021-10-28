from ipgm.Result import *
import random
import copy

def simulOneRes(res: Result, stdev: float) -> Result:
	rp = res.toPercentages()
	rr = copy.deepcopy(rp)
	for i in rp.getCandidates():
		rr.results[i] = random.gauss(rr.results[i], stdev)
	return rr