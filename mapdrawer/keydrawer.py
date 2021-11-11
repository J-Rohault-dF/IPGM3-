from math import pi
from mapdrawer.colors import *
from ipgm.utils import *
import xml.etree.ElementTree as etree


#Useful functions:
#Draw rectangle of a color
def drawRectangle(x0: float, y0: float, width: float, height: float, fill: Color) -> etree.Element:
	return etree.Element('rect', attrib={
		'style': 'fill:{fill};stroke:none;stroke-width:0;stroke-linejoin:round'.format(fill=fill),
		'id': 'rect-{id}'.format(id=getRandomAlphanumeric(6)),
		'width': str(width),
		'height': str(height),
		'x': str(x0),
		'y': str(y0),
	})

#Draw bars

#Write text
def drawText(text: str, x0: float, y0: float, fontSize: float, align: str) -> etree.Element:
	givenId = getRandomAlphanumeric(6)
	t = etree.Element('text', attrib={
		'style': 'font-size:{fontSize}px;line-height:1;font-family:Ubuntu;stroke-width:0;text-anchor:{align};text-align:{align};'.format(fontZier=fontSize, align=align),
		'x': str(x0),
		'y': str(y0),
		'id': 'text-{id}'.format(id=givenId),
	}, )
	t.append(etree.Element('tspan', attrib={
		'style': 'stroke-width:0;text-anchor:{align};text-align:{align};'.format(align=align),
		'x': str(x0),
		'y': str(y0),
		'id': 'tspan-{id}'.format(id=givenId),
		'text': text
	}))

#Write percentages legend

#Draw whole candidate bar
def drawCandidate(name: str, score: float):
	#Write name
	#Draw bar with percentage
	#Put key boxes
	pass

#Draw score circle
def drawPercRing(centerPoint: set[float, float], outerRadius: float, innerRadius: float, percs: list[float], colors: list[Color]) -> set[list[etree.Element], etree.Element]:
	percs = percentList(percs)

	cx,cy = centerPoint[0], centerPoint[1]

	#Convert perc and color to list of sets (start, begin, color)
	rings = []
	run = 0
	for i in range(len(percs)):
		rings.append( (
			(run)*2*pi - (pi/2),
			(percs[i]+run)*2*pi - (pi/2),
			colors[i]
		) )
		run += percs[i]
	
	#Make the mask
	maskId = getRandomAlphanumeric(6)
	mask: list[etree.Element] = []
	mask.append(etree.Element('inkscape:path-effect', attrib={
		'effect': 'powermask',
		'id': 'path-effect-{id}'.format(id=maskId),
		'is_visible': 'true',
		'lpeversion': '1',
		'uri': '#mask-powermask-path-effect-{id}'.format(id=maskId),
		'invert': 'false',
		'hide_mask': 'false',
		'background': 'true',
		'background_color': '#ffffffff',
	}))
	mask.append(etree.Element('svg:mask', attrib={
		'maskUnits': 'userSpaceOnUse',
		'id': 'mask-powermask-path-effect-{id}'.format(id=maskId),
	}))
	mask[1].append(etree.Element('svg:path', attrib={
		'id': 'mask-powermask-path-effect-{id}_box'.format(id=maskId),
		'style': 'fill:#ffffff;fill-opacity:1',
		'd': 'M {cxmo},{cymo} H {cypo} v {cxpo} h -{cymo} z'.format(cxpo=(cx+outerRadius), cypo=(cy+outerRadius), cxmo=(cx-outerRadius), cymo=(cy-outerRadius)),
	}))
	mask[1].append(etree.Element('svg:circle', attrib={
		'style': 'fill:#000000;stroke:none;stroke-width:5;stroke-linejoin:round',
		'id': 'circle-mask-{id}'.format(id=maskId),
		'cx': str(cx),
		'cy': str(cy),
		'r': str(innerRadius),
		'd': 'm {cxpi},{cy} a {r},{r} 0 0 1 -{r},{r} {r},{r} 0 0 1 -{r},-{r} {r},{r} 0 0 1 {r},-{r} {r},{r} 0 0 1 {r},{r} z'.format(cx=cx, cy=cy, r=innerRadius, cxpi=(cx+innerRadius)),
	}))

	mask.append(etree.Element('svg:filter', attrib={
		'id': 'mask-powermask-path-effect-{id}_inverse'.format(id=maskId),
		'inkscape:label': 'filtermask-powermask-path-effect-{id}'.format(id=maskId),
		'style': 'color-interpolation-filters:sRGB',
		'height': '100',
		'width': '100',
		'x': '-50',
		'y': '-50',
	}))
	mask[2].append(etree.Element('svg:feColorMatrix', attrib={
		'id': 'mask-powermask-path-effect-{id}_primitive1'.format(id=maskId),
		'values': '1',
		'type': 'saturate',
		'result': 'fbSourceGraphic',
	}))
	mask[2].append(etree.Element('svg:feColorMatrix', attrib={
		'id': 'mask-powermask-path-effect-{id}_primitive2'.format(id=maskId),
		'values': '-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 1 0 ',
		'in': 'fbSourceGraphic',
	}))

	#Then convert that to the texts
	ringSegments = etree.Element('svg:g', attrib={})
	
	for i in rings:
		ringSegments.append(etree.Element('path', attrib={
			'inkscape:path-effect': '#path-effect-{maskId}'.format(maskId=maskId),
			'd': 'm 88.211234,12.28561 a 5,5 0 0 1 4.390368,2.614692 5,5 0 0 1 -0.199433,5.106091 l -4.194916,-2.720785 z',
			'mask': 'url(#mask-powermask-path-effect-{maskId})'.format(maskId=maskId),
			'id': 'path-{id}'.format(id=getRandomAlphanumeric(6)),
			'sodipodi:type': 'arc',
			'sodipodi:cx': str(centerPoint[0]),
			'sodipodi:cy': str(centerPoint[1]),
			'sodipodi:rx': str(outerRadius),
			'sodipodi:ry': str(outerRadius),
			'sodipodi:start': str(i[0]),
			'sodipodi:end': str(i[1]),
			'sodipodi:arc-type': 'slice',
			'style': 'fill:{color};stroke:none;stroke-width:5;stroke-linejoin:round'.format(color=i[2]),
		}))
	
	#Then return that along with the mask
	return (mask, ringSegments)

