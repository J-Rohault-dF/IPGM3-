from __future__ import annotations
from ipgm.Result import *
import math

def filterThreshold(res: Result, threshold: float = 0) -> dict[str, float]:
	r = res.getCleanResults()
	return {k: v for k,v in sorted(r.items(), key=lambda x: x[1], reverse=True) if (v/sum(r.values()) > threshold)}



def proportionalLargestRemainder(r: dict[str, float], sn: int, quotaType: str) -> dict[str, int]:
	if '@' in r: del r['@']

	vn = sum(r.values())

	if quotaType == 'Hare': quota = vn / sn
	elif quotaType == 'Droop': quota = (vn / (sn + 1)) + 1
	elif quotaType == 'HB' or quotaType == 'Hagenbach-Bischoff': quota = vn / (sn + 1)
	elif quotaType == 'Imperiali': quota = vn / (sn + 2)

	#First pass
	seats = {k: math.floor(v/quota) for k,v in r.items()}

	#Second pass
	remaining = sn - sum(seats.values())
	remainders = ((k, (v-quota*seats[k])) for k,v in r.items())
	remainders = sorted(remainders, key=lambda x: x[1], reverse=True)
	for k in remainders[:remaining]:
		seats[k[0]] += 1

	return seats



def getDivisor(seats: int, methodType: str) -> float:
	if methodType == 'D\'Hondt': return (seats+1)
	elif methodType == 'Webster' or methodType == 'Sainte-Laguë': return (seats+0.5)
	elif methodType == 'Imperiali': return (seats+2)
	elif methodType == 'Huntington-Hill': return (seats*(seats+1)) ** 0.5
	elif methodType == 'Danish': return (seats+(1/3))
	elif methodType == 'Adams': return (seats)

def proportionalHighestAverage(r: dict[str, float], sn: int, methodType: str) -> dict[str, int]:

	seats = {x[0]: (0 if methodType not in ['Huntington-Hill', 'Adams'] else 1) for x in sorted(r.items(), key=lambda x: x[1], reverse=True)}

	averages = {k: (v/getDivisor(seats[k], methodType)) for k,v in r.items()}

	while sum(seats.values()) < sn:

		highest = sorted(averages.items(), key=lambda x: x[1], reverse=True)[0][0]
		seats[highest] += 1
		averages[highest] = (r[highest]/getDivisor(seats[highest], methodType))
	
	return seats



def twoRoundProportional(d1: dict[str, float], d2: dict[str, float], sn: int) -> dict[str, int]:
	
	halfSeats = math.floor(sn/2)

	#Run both rounds
	if halfSeats > 0:
		t1 = proportionalLargestRemainder(d1, halfSeats, 'Hare')
		t2 = proportionalLargestRemainder(d2, halfSeats, 'Hare')
	else:
		t1,t2 = {k: 0 for k in d1.keys()}, {k: 0 for k in d2.keys()}

	seats = {k: (v+(t2[k] if k in t2 else 0)) for k,v in t1.items()} #Add the seats from r1 and r2

	#If one seat remains
	if (sn%2 == 1):
		remainders = {k: v for k,v in d1.items()} #Take the r1 values
		for k,v in d2.items():
			remainders[k] += v #Add the r2 values
		remainders = {k: (v/sum(remainders.values())) for k,v in remainders.items()} #Divide to get percentages - not sure it's needed

		#Calculate the running score
		remainders = {k: v/(t1[k]+(t2[k] if k in t2 else 0)+1) for k,v in remainders.items()}

		kM,vM = '',0
		for k,v in remainders.items():
			if v > vM:
				vM = v
				kM = k

		seats[kM] += 1 #Add the excess seat
	
	return seats