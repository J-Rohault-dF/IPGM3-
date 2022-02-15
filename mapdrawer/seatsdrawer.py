import xml.etree.ElementTree as etree
from ipgm.utils import *
from colour import *
import math

seatsArrangements: dict[int, dict[str, list[int]]] = {
	0: {'Regular': []},
	1: {'Regular': [1]},
	2: {'Regular': [2]},
	3: {'Regular': [2, 1]},
	4: {'Regular': [2, 2]},
	5: {'Regular': [3, 2]},
	6: {'Regular': [3, 3]},
	7: {'Regular': [2, 3, 2], 'Wide': [4, 3]},
	8: {'Regular': [3, 3, 2], 'Wide': [4, 4], 'Long': [2, 2, 2, 2]},
	9: {'Regular': [3, 3, 3], 'Wide': [5, 4], 'Long': [2, 2, 2, 2, 1]},
	10: {'Regular': [3, 4, 3]},
	11: {'Regular': [4, 4, 3]},
	12: {'Regular': [4, 4, 4]},
	12: {'Regular': [4, 4, 4]},
	13: {'Regular': [4, 5, 4]},
	14: {'Regular': [5, 5, 4], 'Wide': [7, 7]},
	15: {'Regular': [5, 5, 5]},
	17: {'Regular': [6, 6, 5]},
	26: {'Regular': [6, 7, 7, 6]},
	28: {'Regular': [5, 6, 6, 6, 5]},
	38: {'Regular': [7, 8, 8, 8, 7]},
	52: {'Regular': [8, 9, 9, 9, 9, 8]},
}

def findSeatsArrangement(totalSeats: int, layout: str, ratio: float = None):
	if totalSeats in seatsArrangements and layout in seatsArrangements[totalSeats]:
		return seatsArrangements[totalSeats][layout]
	else:
		squareSide = math.ceil(totalSeats**(1/2) * (ratio if ratio != None else 1))
		arrangement = []
		while totalSeats > 0:
			arrangement.append(min(squareSide, totalSeats))
			totalSeats -= arrangement[-1]
		return arrangement



def argsFind(l: list[list], s: str) -> int:
	for i in range(len(l)):
		if l[i][0] == s: return i
	return None

def replaceFill(s: str, f: Color) -> str:
	args = [l.split(':') for l in s.split(';')]
	args[argsFind(args, 'fill')] = ['fill', str(f)]
	return ';'.join([':'.join(x) for x in args])


#Function to draw 1 circle (with given id)
def drawOneCircle(pos: set[float, float], givenId: str, radius: float, strokeWidth, fillColor: Color = Color('#c0c0c0'), strokeColor: Color = Color('#000000')) -> etree.Element:
	circle = etree.Element('{http://www.w3.org/2000/svg}circle', attrib={
		'style': 'fill:{fillColor};fill-opacity:1;stroke:{strokeColor};stroke-width:{strokeWidth};stroke-miterlimit:4;stroke-dasharray:none;stroke-opacity:1'.format(fillColor=fillColor, strokeColor=strokeColor, strokeWidth=strokeWidth),
		'id': givenId,
		'cx': str(pos[0]),
		'cy': str(pos[1]),
		'r': str(radius),
	})
	return circle

def genAlternating(layout: list[int], reverse: bool = False): #Terrible implementation, please don't look at this code
	cols = [[] for x in layout]
	scores = [x/2 for x in layout]
	counter = 0
	i = 0
	while counter < sum(flattenList(layout)):
		j = len(layout)-i-1
		if scores[j] == max(scores):
			cols[j].append(counter if not reverse else (sum(layout)-counter-1))
			scores[j] -= 1
			counter += 1
		i = (i+1)%len(layout)
	return flattenList(cols)



#Function to draw N circles (with given dept id)
def drawCircles(seatsData: dict[str, str|int], givenId: str, circlesSize: float, strokeSize: float, distanceBetweenCenters: float) -> etree.Element:
	circles = etree.Element('{http://www.w3.org/2000/svg}g', attrib={'id': 'seats-circles-{gid}'.format(gid=givenId)})
	
	cx, cy = seatsData['cx'], seatsData['cy']
	orient = seatsData['orientation']
	ratio = float(seatsData['ratio'])
	if ratio == 0: ratio = None
	totalSeats = int(seatsData['seats'])
	
	#Find the seats layout
	seatsLayout = findSeatsArrangement(totalSeats, seatsData['layout'], ratio)
	fullHeight = (len(seatsLayout)-1)*distanceBetweenCenters
	counter = 0

	seatsNumbers = []
	if orient == '' or orient == 0: seatsNumbers = [x for x in range(0, totalSeats)]
	elif orient == 'M': seatsNumbers = [totalSeats-x for x in range(0, totalSeats)] #Mirror
	elif orient == 'R':
		circles.set('transform', 'rotate(90,{cx},{cy})'.format(cx=cx, cy=cy))
		seatsNumbers = genAlternating(seatsLayout)
	elif orient == 'L':
		circles.set('transform', 'rotate(-90,{cx},{cy})'.format(cx=cx, cy=cy))
		seatsNumbers = genAlternating(seatsLayout, reverse=True)

	#Create the circles and put them all in the group
	for ri in range(len(seatsLayout)):
		row = seatsLayout[ri]
		#Get the leftmost circle
		rowLength = (row-1)*distanceBetweenCenters
		for ci in range(row):
			cPos = (cx-(rowLength/2)+(distanceBetweenCenters*ci), cy-(fullHeight/2)+(distanceBetweenCenters*ri))
			circles.append(drawOneCircle(cPos, 'circle-{gid}-{n}'.format(gid=givenId, n=seatsNumbers[counter]), circlesSize, strokeSize, Color('#c0c0c0')))
			counter += 1

	return circles

def colorCircles(seats: etree.Element, searchId: str, data: list[set[Color, int]]) -> etree.Element:

	colors = unpackPairSets(data)

	if sum([x[1] for x in data]) != len(seats):
		#TODO: Implement this
		raise ValueError('Seats for {sid} have {n} seats but are being modified to have {ni}'.format(sid=searchId, n=len(seats), ni=sum([x[1] for x in data])))
	
	counter = 0
	for i in range(len([x for x in seats.iter()][1:])):
		s = [x for x in seats.iter() if x.get('id') == 'circle-{gid}-{n}'.format(gid=searchId.replace(' ','-'), n=i)][0]
		s.set('style', replaceFill(s.get('style'), colors[counter]))
		counter += 1
	
	return seats

def getCenter(e: etree.Element) -> set[float, float]:
	if e.get('{http://en.wikipedia.org/wiki/Main_Page}cx') == None: return (0, 0)
	return (float(e.get('{http://en.wikipedia.org/wiki/Main_Page}cx')), float(e.get('{http://en.wikipedia.org/wiki/Main_Page}cy')))
