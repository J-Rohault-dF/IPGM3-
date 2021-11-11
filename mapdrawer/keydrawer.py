from math import pi
from mapdrawer.colors import *
from ipgm.utils import *
import xml.etree.ElementTree as etree

def textToElement(t: str) -> etree.Element:
	t = '<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg xmlns:svg="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns="http://www.w3.org/2000/svg" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd">'+t+'</svg>'
	e = etree.fromstring(t)
	e = [x for x in e][0]
	return e

def textToElements(t: str) -> list[etree.Element]:
	t = '<?xml version="1.0" encoding="UTF-8" standalone="no"?><svg xmlns:svg="http://www.w3.org/2000/svg" xmlns:inkscape="http://www.inkscape.org/namespaces/inkscape" xmlns="http://www.w3.org/2000/svg" xmlns:sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd">'+t+'</svg>'
	e = etree.fromstring(t)
	el = [x for x in e]
	return el



#Useful functions:
#Draw rectangle of a color
def drawRectangle(x0: float, y0: float, width: float, height: float, fill: Color) -> etree.Element:
	return textToElement('<rect style="fill:{fill};stroke:none;stroke-width:0;stroke-linejoin:round" id="rect-{id}" width="{width}" height="{height}" x="{x0}" y="{y0}" />'.format(fill=fill, id=getRandomAlphanumeric(6), width=width, height=height, x0=x0, y0=y0))

#(find highest used id in svg)

#Draw bars

#Write text
def drawText(text: str, x0: float, y0: float, fontSize: float, align: str, id: str) -> etree.Element:
	return textToElement('''<text style="font-size:{fontSize}px;line-height:1;font-family:Ubuntu;stroke-width:0;text-anchor:{align};text-align:{align};" x="{x0}" y="{y0}" id="text-{id}"><tspan id="textspan-{id}" x="33.141422" y="{y0}" style="stroke-width:0;text-anchor:{align};text-align:{align};">{text}</tspan></text>'''.format(align=align, fontSize=fontSize, x0=x0, y0=y0, id=getRandomAlphanumeric(6), text=text))

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
	mask = """<inkscape:path-effect
effect="powermask"
id="path-effect-{id}"
is_visible="true"
lpeversion="1"
uri="#mask-powermask-path-effect-{id}"
invert="false"
hide_mask="false"
background="true"
background_color="#ffffffff" />
<mask
maskUnits="userSpaceOnUse"
id="mask-powermask-path-effect-{id}">
<path
id="mask-powermask-path-effect-{id}_box"
style="fill:#ffffff;fill-opacity:1"
d="M {cxmo},{cymo} H {cypo} v {cxpo} h -{cymo} z" />
<circle
style="fill:#000000;stroke:none;stroke-width:5;stroke-linejoin:round"
id="circle-mask-{id}"
cx="{cx}"
cy="{cy}"
r="{r}"
d="m {cxpi},{cy} a {r},{r} 0 0 1 -{r},{r} {r},{r} 0 0 1 -{r},-{r} {r},{r} 0 0 1 {r},-{r} {r},{r} 0 0 1 {r},{r} z" />
</mask>
<filter
id="mask-powermask-path-effect-{id}_inverse"
inkscape:label="filtermask-powermask-path-effect-{id}"
style="color-interpolation-filters:sRGB"
height="100"
width="100"
x="-50"
y="-50">
<feColorMatrix
id="mask-powermask-path-effect-{id}_primitive1"
values="1"
type="saturate"
result="fbSourceGraphic" />
<feColorMatrix
id="mask-powermask-path-effect-{id}_primitive2"
values="-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 1 0 "
in="fbSourceGraphic" />
</filter>""".format(id=maskId, cx=cx, cy=cy, r=innerRadius, ro=outerRadius, cxpi=(cx+innerRadius), cxpo=(cx+outerRadius), cypo=(cy+outerRadius), cxmo=(cx-outerRadius), cymo=(cy-outerRadius))
	mask = textToElements(mask)

	#Then convert that to the texts
	allTexts = []
	for i in rings:
		curText = """<path
style="fill:{color};stroke:none;stroke-width:5;stroke-linejoin:round"
id="path-{id}"
sodipodi:type="arc"
sodipodi:cx="{cx}"
sodipodi:cy="{cy}"
sodipodi:rx="{r}"
sodipodi:ry="{r}"
sodipodi:start="{start}"
sodipodi:end="{end}"
sodipodi:arc-type="slice"
d="m 88.211234,12.28561 a 5,5 0 0 1 4.390368,2.614692 5,5 0 0 1 -0.199433,5.106091 l -4.194916,-2.720785 z"
mask="url(#mask-powermask-path-effect-{maskId})"
inkscape:path-effect="#path-effect-{maskId}" />""".format(id=getRandomAlphanumeric(6), cx=centerPoint[0], cy=centerPoint[1], r=outerRadius, start=i[0], end=i[1], color=i[2], maskId=maskId)
		allTexts.append(curText)
	
	ringSegments = textToElement('<g>'+'\n'.join(allTexts)+'</g>')
	
	#Then return that along with the mask
	return (mask, ringSegments)

