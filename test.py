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

#from ipgm.port import *
#t1 = loadDataTable('data/2017T1.csv')

coords = """\
147.709	44.947
143.658	52.113
126.546	58.795
122.715	14.194
136.949	53.109
141.593	68.596
130.476	67.695
174.178	21.299
130.476	16.838
107.586	23.239
115.432	17.501
141.919	58.960
163.744	23.668
130.245	41.457
99.035	15.613
125.275	19.959
141.341	40.301
115.585	36.178
145.965	18.225
103.572	18.987
132.903	57.755
103.449	14.217"""

coords = [[float(y) for y in x.split('\t')] for x in coords.split('\n')]
coords = [[x[0]+4, x[1]] for x in coords]

print('x:')
print('\n'.join(str(x[0]) for x in coords))
print('y:')
print('\n'.join(str(x[1]) for x in coords))

#coords = '\n'.join(['\t'.join([str(y) for y in x]) for x in coords])