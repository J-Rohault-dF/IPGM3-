from ipgm.Result import *
import math

def proportionalLargestRemainder(res: Result, sn: int, quotaType: str, threshold: float = 0) -> dict[str, int]:

	r = res.results
	r = {k: v for k,v in sorted(r.items(), key=lambda x: x[1], reverse=True) if (v/sum(r.values()) > threshold)}
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

def proportionalHighestAverage(res: Result, sn: int, methodType: str, threshold: float = 0) -> dict[str, int]:

	r = res.results
	r = {k: v for k,v in r.items() if (v/sum(r.values()) > threshold)}
	seats = {x[0]: (0 if methodType not in ['Huntington-Hill', 'Adams'] else 1) for x in sorted(r.items(), key=lambda x: x[1], reverse=True)}

	averages = {k: (v/getDivisor(seats[k], methodType)) for k,v in r.items()}

	while sum(seats.values()) < sn:

		highest = sorted(averages.items(), key=lambda x: x[1], reverse=True)[0][0]
		seats[highest] += 1
		averages[highest] = (r[highest]/getDivisor(seats[highest], methodType))
	
	return seats