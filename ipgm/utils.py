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