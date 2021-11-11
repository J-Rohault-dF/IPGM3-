import random

def sumProductDict(a: dict, b: dict) -> float:
	allKeys = unionLists(list(a.keys()), list(b.keys()))
	c = 0
	for k in allKeys:
		if (k in a.keys()) and (k in b.keys()):
			c += float(a[k])*float(b[k])
	return c

def sumDict(d: dict) -> float:
	return sum(d.values())

def multiplyDict(d: dict, n: float) -> dict:
	return {k: v*n for k,v in d.items()}

#Multiplies all values in a 2d matrix by 0.01
def percentMatrix(m: list) -> list:
	for i in range(len(m)):
		m[i] = [x*0.01 for x in m[i]]
	return m

def mean(l: list) -> float:
	return sum(l)/len(l)

def mean(d: dict) -> float:
	return sum(d.values())/len(d)

#Unpacks divisions from otherCollectivites
def unpackDivisions(name: str, originalList: list, unpackingList: dict) -> list:
	#Recursive function, find name in unpackingList then call itself on each of its components until you find something on originalList

	if name in originalList: return [name]

	v = unpackingList[name]
	allDivs = [unpackDivisions(x, originalList, unpackingList) for x in v]
	allDivs = flattenList(allDivs)

	return allDivs

#Flattens a list, not recursive (only does 1 level), but apparently it's recursive (I just checked)
def flattenList(li: list) -> list:
	lf = []
	for l in li:
		if type(l) is list: lf += flattenList(l)
		else: lf.append(l)
	return lf

#Computes the union of elements of two lists
def unionLists(l1: list, l2: list) -> list:
	lf = list(l1)
	for e in list(l2):
		if e not in lf: lf.append(e)
	return lf

#Replaces every value with their share of the total list
def percentList(l: list) -> list:
	return [x/sum(l) for x in l]

#Replaces every value with their share of the total dict
def percentDict(d: dict) -> dict:
	return {k: v/sum(d.values()) for k,v in d.items()}

#Gets the args in a .vtm file
def getArgs(args: list, k: str) -> list:
	return [x[1:] for x in args if x[0] == k]

#Returns list with no doubles
def getSetList(l: list) -> list:
	lf = []
	for e in l:
		if e not in lf: lf.append(e)
	return lf

def formatPerc(n: float) -> str:
	n = str(round(float(n)*100, 1))
	if '.' not in n: n+='.0'
	return n+'%'

def averageList(l: list) -> float:
	return sum(l)/len(l)

def allEquals(l: list) -> bool:
	p = l[0]
	for i in l:
		if i != p: return False
	return True

def getProbsFromResDict(d: dict) -> set[str, float]:
	d = {k: v for k,v in sorted(d.items(), key=lambda item: item[1], reverse=True)}
	k1, k2 = list(d.keys())[0], list(d.keys())[1]
	m = d[k1] - d[k2]
	
	return (k1, m)

def getRankInDict(d: dict, s: str):
	ls = [k for k in sorted(d.keys(), key=lambda x: d[x], reverse=True)]
	return ls.index(s)

def appendInDict(d: dict[str, list], k, v):
	if k in d.keys(): d[k].append(v)
	else: d[k] = [v]

def appendDictInDict(d: dict[str, dict], dk, k, v):
	if dk in d.keys(): d[dk][k] = v
	else: d[dk] = {k: v}

def unpackPairSets(s: set) -> list:
	l = []
	for k,v in s:
		l += [k]*v
	return l

def getRandomAlphanumeric(k: int):
	return ''.join(random.choices(list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'), k=k))