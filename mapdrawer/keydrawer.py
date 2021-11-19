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

#Draw score ring behind
def drawPercRingBehind(centerPoint: set[float, float], innerRadius: float, outerRadius: float, factor: float, fillColor: Color = Color('#000000')):
	
	margin = (outerRadius-innerRadius)*factor
	innerRadius -= margin
	outerRadius += margin

	maskId, mask = createMask(centerPoint, innerRadius, outerRadius)

	return (mask, etree.Element('{http://www.w3.org/2000/svg}path', attrib={
		'd': 'm 88.211234,12.28561 a 5,5 0 0 1 4.390368,2.614692 5,5 0 0 1 -0.199433,5.106091 l -4.194916,-2.720785 z',
		'mask': 'url(#mask-powermask-path-effect-{maskId})'.format(maskId=maskId),
		'id': 'path-{id}'.format(id=getRandomAlphanumeric(6)),
		'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}type': 'arc',
		'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cx': str(centerPoint[0]),
		'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cy': str(centerPoint[1]),
		'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}rx': str(outerRadius),
		'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}ry': str(outerRadius),
		'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}start': '0',
		'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}end': '0',
		'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}arc-type': 'slice',
		'style': 'fill:{color};stroke:none;stroke-width:5;stroke-linejoin:round'.format(color=fillColor),
	}))



#Draw score ring
def drawPercRing(centerPoint: set[float, float], outerRadius: float, innerRadius: float, percs: list[float], colors: list[Color]) -> set[list[etree.Element], etree.Element]:
	percs = list(reversed(percentList(percs)))
	colors = list(reversed(colors))

	#Convert perc and color to list of sets (start, begin, color)
	rings = []
	run = 0
	for i in range(len(percs)):
		if percs[i] == 0: continue

		rings.append( (
			(run)*2*pi - (pi/2),
			(percs[i]+run)*2*pi - (pi/2),
			colors[i]
		) )
		run += percs[i]
	
	maskId, mask = createMask(centerPoint, innerRadius, outerRadius)

	#Then convert that to the texts
	ringSegments = etree.Element('{http://www.w3.org/2000/svg}g', attrib={
		'{http://www.inkscape.org/namespaces/inkscape}path-effect': '#path-effect-{maskId}'.format(maskId=maskId), #Just putting this comment here in remembrance of the fact that this function only started working correctly ten days after it was written, because this attribute was put for each ring segment while it should be applied to the entire group. 2021-11-09 - 2021-11-18 (and thanks to Nathan Lee for pointing this out on the inkscape gitlab)
	})
	
	for i in rings:
		ringSegments.append(etree.Element('{http://www.w3.org/2000/svg}path', attrib={
			'd': 'm 88.211234,12.28561 a 5,5 0 0 1 4.390368,2.614692 5,5 0 0 1 -0.199433,5.106091 l -4.194916,-2.720785 z',
			'mask': 'url(#mask-powermask-path-effect-{maskId})'.format(maskId=maskId),
			'id': 'path-{id}'.format(id=getRandomAlphanumeric(6)),
			'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}type': 'arc',
			'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cx': str(centerPoint[0]),
			'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}cy': str(centerPoint[1]),
			'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}rx': str(outerRadius),
			'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}ry': str(outerRadius),
			'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}start': str(i[0]),
			'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}end': str(i[1]),
			'{http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd}arc-type': 'slice',
			'style': 'fill:{color};stroke:none;stroke-width:5;stroke-linejoin:round'.format(color=i[2]),
		}))
	
	#Then return that along with the mask
	return (mask, ringSegments)





def createMask(centerPoint: set[float, float], innerRadius: float, outerRadius: float):
	
	cx,cy = centerPoint[0],centerPoint[1]

	maskId = getRandomAlphanumeric(6)

	mask: list[etree.Element] = []
	mask.append(etree.Element('{http://www.inkscape.org/namespaces/inkscape}path-effect', attrib={
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
	mask.append(etree.Element('{http://www.w3.org/2000/svg}mask', attrib={
		'maskUnits': 'userSpaceOnUse',
		'id': 'mask-powermask-path-effect-{id}'.format(id=maskId),
	}))
	mask[1].append(etree.Element('{http://www.w3.org/2000/svg}path', attrib={
		'id': 'mask-powermask-path-effect-{id}_box'.format(id=maskId),
		'style': 'fill:#ffffff;fill-opacity:1',
		'd': 'M {cxmo},{cymo} h {o2} v {o2} h {no2} z'.format(o2=(outerRadius*2), no2=-(outerRadius*2), cxmo=(cx-outerRadius), cymo=(cy-outerRadius)),
	}))
	mask[1].append(etree.Element('{http://www.w3.org/2000/svg}circle', attrib={
		'style': 'fill:#000000;stroke:none;stroke-width:5;stroke-linejoin:round',
		'id': 'circle-mask-{id}'.format(id=maskId),
		'cx': str(cx),
		'cy': str(cy),
		'r': str(innerRadius),
		'd': 'm {cxpi},{cy} a {r},{r} 0 0 1 -{r},{r} {r},{r} 0 0 1 -{r},-{r} {r},{r} 0 0 1 {r},-{r} {r},{r} 0 0 1 {r},{r} z'.format(cx=cx, cy=cy, r=innerRadius, cxpi=(cx+innerRadius)),
	}))

	mask.append(etree.Element('{http://www.w3.org/2000/svg}filter', attrib={
		'id': 'mask-powermask-path-effect-{id}_inverse'.format(id=maskId),
		'{http://www.inkscape.org/namespaces/inkscape}label': 'filtermask-powermask-path-effect-{id}'.format(id=maskId),
		'style': 'color-interpolation-filters:sRGB',
		'height': '100',
		'width': '100',
		'x': '-50',
		'y': '-50',
	}))
	mask[2].append(etree.Element('{http://www.w3.org/2000/svg}feColorMatrix', attrib={
		'id': 'mask-powermask-path-effect-{id}_primitive1'.format(id=maskId),
		'values': '1',
		'type': 'saturate',
		'result': 'fbSourceGraphic',
	}))
	mask[2].append(etree.Element('{http://www.w3.org/2000/svg}feColorMatrix', attrib={
		'id': 'mask-powermask-path-effect-{id}_primitive2'.format(id=maskId),
		'values': '-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 1 0 ',
		'in': 'fbSourceGraphic',
	}))
	
	return maskId,mask