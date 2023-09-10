from ipgm.Result import *
import ipgm.Div
import math
import typing

def filterThreshold(res: Result, threshold: float = 0) -> dict[str, float]:

	#really ugly fix but i don't have the energy to rewrite everything
	if res is None: return {}
	if type(res) == ipgm.Div.Div: res = res.result
	#

	r = res.getCleanResults()
	return {k: v for k,v in sorted(r.items(), key=lambda x: x[1], reverse=True) if (v/sum(r.values()) > threshold)}



def getHareQuota(votes: float, seats: int) -> float: return votes/seats

def getDroopQuota(votes: float, seats: int) -> float: return (votes/(seats+1)) + 1

def getHagenbachBischoffQuota(votes: float, seats: int) -> float: return votes/(seats+1)

def getImperialiQuota(votes: float, seats: int) -> float: return votes/(seats+2)

def proportionalLargestRemainder(r: dict[str, float], sn: int, quotaMethod: typing.Callable[[float, int], float]) -> dict[str, int]:
	if hasNonExpressed(r):
		for i in allNonExpressed(r):
			del r[i]

	vn = sum(r.values())
	
	quota = quotaMethod(vn, sn)

	#First pass
	seats = {k: math.floor(v/quota) for k,v in r.items() if isCandidate(k)}

	#Second pass
	remaining = int(sn - sum(seats.values()))
	remainders = ((k, (v-quota*seats[k])) for k,v in r.items() if isCandidate(k))
	remainders = sorted(remainders, key=lambda x: x[1], reverse=True)
	for k in remainders[:remaining]:
		seats[k[0]] += 1

	return seats



def getDHondtDivisor(seats: int) -> float: return (seats+1)

def getWebsterDivisor(seats: int) -> float: return (seats+0.5)

def getImperialiDivisor(seats: int) -> float: return (seats+2)

def getHuntingtonHillDivisor(seats: int) -> float: return (seats*(seats+1)) ** 0.5

def getDanishDivisor(seats: int) -> float: return (seats+(1/3))

def getAdamsDivisor(seats: int) -> float: return seats

def proportionalHighestAverage(r: dict[str, float], sn: int, divisor: typing.Callable[[int], float]) -> dict[str, int]:
	
	if r == {}: return {}

	seats = {x[0]: (0 if divisor not in [getHuntingtonHillDivisor, getAdamsDivisor] else 1) for x in sorted(r.items(), key=lambda x: x[1], reverse=True) if isCandidate(x[0])}

	averages = {k: (v/divisor(seats[k])) for k,v in r.items() if isCandidate(k)}

	while sum(seats.values()) < sn:

		highest = sorted(averages.items(), key=lambda x: x[1], reverse=True)[0][0]
		seats[highest] += 1
		averages[highest] = (r[highest]/divisor(seats[highest]))
	
	return seats



def twoRoundProportional(d1: dict[str, float], d2: dict[str, float], sn: int) -> dict[str, int]:
	
	halfSeats = math.floor(sn/2)

	#Run both rounds
	if halfSeats > 0:
		t1 = proportionalLargestRemainder(d1, halfSeats, getHareQuota)
		t2 = proportionalLargestRemainder(d2, halfSeats, getHareQuota)
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



'''def apparentementsProportional(votes: dict[str, float], sn: int, quotaType: str, apparentements: list[str]):
	
	#Make list of apparentements
	apparentementsList = {party: [[party], votes] for party,votes in votes.items()}
	
	for party in votes.keys():
		for i,apparentement in enumerate(apparentements):
			if party in apparentement:
				apparentementName = '-'.join(apparentement)
				if apparentementName not in apparentementsList: apparentementsList[apparentementName] = [[], 0]
				apparentementsList[apparentementName] = [apparentementsList[apparentementName][0]+[party], apparentementsList[apparentementName][1]+apparentementsList[party][1]]
				del apparentementsList[party]
				break

	#Distribute seats
	print(apparentementsList)
	seatsTotal = proportionalLargestRemainder({k: v[1] for k,v in apparentementsList.items()}, sn, quotaType)

	#Distribute seats within apparentements
	for apparentementName, apparentement in apparentementsList.items():
		apparentedParties, apparentementVotes = apparentement[0], apparentement[1]

		apparentementResults = {p: v for p,v in votes.items() if p in apparentedParties}

		print(seatsTotal[apparentementName], apparentementResults)
		seatsInApparentement = proportionalLargestRemainder(apparentementResults, seatsTotal[apparentementName], quotaType)

		seatsTotal = seatsTotal | seatsInApparentement
		del seatsTotal[apparentementName]

	return seatsTotal



class TestApparentementsProportional(unittest.TestCase):

	def test_apparentementsProportional(self):
		self.assertEqual(
			apparentementsProportional(votes={'A': 1, 'B': 2, 'C': 3}, sn=2, quotaType='Hare', apparentements=[['A', 'B']]),
			{'B': 1, 'C': 1}
		)

if __name__ == '__main__':
	unittest.main()'''