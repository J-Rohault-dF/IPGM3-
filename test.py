from mapdrawer.keydrawer import *
from mapdrawer.seatsdrawer import *
from ipgm.Result import *
from ipgm.ResultsSet import *
from ipgm.proportional import *
from simulvote.simul import *
import xml.etree.ElementTree as etree

#with open('data/svg_test_2.svg', 'r') as svgdoc:
#	xmlR = etree.parse(svgdoc)
#
##scores = [155, 139, 538, 946, 476]
##colors = [Color('#351049'), Color('#549103'), Color('#865910'), Color('#967414'), Color('#549310')]
#
##a, b = drawPercRing((40, 40), 5, 3, scores, colors)
#
#seats = drawCircles((0, 0), ((Color("red"), 5), (Color("blue"), 3)), 2.2777781, 0.569444, 5.52238)
#
#root = xmlR.getroot()
##root.find('{http://www.w3.org/2000/svg}defs').extend(a)
##root.find('{http://www.w3.org/2000/svg}g').append(b)
#root.find('{http://www.w3.org/2000/svg}g').append(seats)
#
#xmlR.write('data/svg_test_2.svg', encoding='unicode')

#res = Result('test', {'a': 2836, 'b': 2763, 'c': 1203, 'd': 16})

from ipgm.port import *
t1 = loadDataTable('data/2017T1.csv')