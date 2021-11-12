import xml.etree.ElementTree as etree
from ipgm.utils import *
from colour import *

seatsArrangements: dict[int, list[int]] = {
	0: [],
	1: [1],
	2: [2],
	3: [1, 2],
	4: [2, 2],
	5: [2, 3],
	6: [3, 3],
	7: [2, 3, 2],
	8: [3, 3, 2],
	9: [3, 3, 3],
	10: [3, 4, 3],
	11: [3, 4, 4],
	12: [4, 4, 4],
	12: [4, 4, 4],
	13: [4, 5, 4],
	14: [5, 5, 4],
	15: [5, 5, 5],
	17: [6, 6, 5],
	26: [6, 7, 7, 6],
	28: [5, 6, 6, 6, 5],
	38: [7, 8, 8, 8, 7],
	52: [8, 9, 9, 9, 9, 8],
}

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

#Function to draw N circles (with given dept id)
def drawCircles(pos: set[float, float], number: int, givenId: str, circlesSize: float, strokeSize: float, distanceBetweenCenters: float) -> etree.Element:
	circles = etree.Element('{http://www.w3.org/2000/svg}g', attrib={'id': 'seats-circles-{gid}'.format(gid=givenId)})
	
	#Find the seats arrangement
	seatsArrangement = seatsArrangements[number]
	fullHeight = (len(seatsArrangement)-1)*distanceBetweenCenters
	counter = 0

	#Create the circles and put them all in the group
	for ri in range(len(seatsArrangement)):
		row = seatsArrangement[ri]
		#Get the leftmost circle
		rowLength = (row-1)*distanceBetweenCenters
		for ci in range(row):
			cPos = (pos[0]-(rowLength/2)+(distanceBetweenCenters*ci), pos[1]-(fullHeight/2)+(distanceBetweenCenters*ri))
			circles.append(drawOneCircle(cPos, 'circle-{gid}-{n}'.format(gid=givenId, n=counter), circlesSize, strokeSize, Color('#c0c0c0')))
			counter += 1

	return circles

def colorCircles(seats: etree.Element, searchId: str, data: list[set[Color, int]]) -> etree.Element:

	colors = unpackPairSets(data)

	if sum([x[1] for x in data]) != len(seats):
		#TODO: Implement this
		raise ValueError('Seats for {sid} have {n} seats but are being modified to have {ni}'.format(sid=searchId, n=len(seats), ni=sum([x[1] for x in data])))
	
	counter = 0
	for s in [x for x in seats.iter()][1:]:
		s.set('style', replaceFill(s.get('style'), colors[counter]))
		counter += 1
	
	return seats

def getCenter(e: etree.Element) -> set[float, float]:
	if e.get('{http://en.wikipedia.org/wiki/Main_Page}cx') == None: return (0, 0)
	return (float(e.get('{http://en.wikipedia.org/wiki/Main_Page}cx')), float(e.get('{http://en.wikipedia.org/wiki/Main_Page}cy')))
