from math import pi
from mapdrawer.colors import *
from ipgm.utils import *

#Useful functions:
#Draw rectangle of a color
def drawRectangle(x0: float, y0: float, width: float, height: float, fill: Color) -> str:
	return '<rect style="fill:{fill};stroke:none;stroke-width:0;stroke-linejoin:round" id="rect-{id}" width="{width}" height="{height}" x="{x0}" y="{y0}" />'.format(fill=fill, id=getRandomAlphanumeric(6), width=width, height=height, x0=x0, y0=y0)

#(find highest used id in svg)

#Draw bars

#Write text
def drawText(text: str, x0: float, y0: float, fontSize: float, align: str, id: str) -> str:
	return '''<text style="font-size:{fontSize}px;line-height:1;font-family:Ubuntu;stroke-width:0;text-anchor:{align};text-align:{align};" x="{x0}" y="{y0}" id="text-{id}"><tspan id="textspan-{id}" x="33.141422" y="{y0}" style="stroke-width:0;text-anchor:{align};text-align:{align};">{text}</tspan></text>'''.format(align=align, fontSize=fontSize, x0=x0, y0=y0, id=getRandomAlphanumeric(6), text=text)

#Write percentages legend

#Draw whole candidate bar
def drawCandidate(name: str, score: float):
	#Write name
	#Draw bar with percentage
	#Put key boxes
	pass

#Draw score circle
def drawPercRing(centerPoint: set[float, float], outerRadius: float, innerRadius: float, percs: list[float], colors: list[Color]):
	percs = percentList(percs)

	cx,cy = centerPoint[0], centerPoint[1]

	#Convert perc and color to list of sets (start, begin, color)
	rings = []
	for i in range(len(percs)):
		rings.append( (
			-pi/2,
			percs[i]*2*pi - (pi/2),
			colors[i]
		) )
	
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
d="m {cxm},{cym} h {ro} v {ro} h -{ro} z" />
<circle
style="fill:#000000;stroke:none;stroke-width:5;stroke-linejoin:round"
id="circle-mask-{id}"
cx="{cx}"
cy="{cy}"
r="{r}"
d="m {cxp},{cy} a {r},{r} 0 0 1 -{r},{r} {r},{r} 0 0 1 -{r},-{r} {r},{r} 0 0 1 {r},-{r} {r},{r} 0 0 1 {r},{r} z" />
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
</filter>""".format(id=maskId, cx=cx, cy=cy, r=innerRadius, ro=outerRadius, cxp=(cx+innerRadius), cxm=(cx-innerRadius), cym=(cy-innerRadius))

	#Then convert that to the texts
	texts = []
	for i in rings:
		texts.append(
			"""<path
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
		)
	
	#Then return that along with the mask
	return (mask, '\n'.join(texts))





#What I'm supposed to get
"""<inkscape:path-effect
       effect="powermask"
       id="path-effect139"
       is_visible="true"
       lpeversion="1"
       uri="#mask-powermask-path-effect139"
       invert="false"
       hide_mask="false"
       background="true"
       background_color="#ffffffff" />
    <mask
       maskUnits="userSpaceOnUse"
       id="mask-powermask-path-effect139">
      <path
         id="mask-powermask-path-effect139_box"
         style="fill:#ffffff;fill-opacity:1"
         d="m 93.966515,133.89844 h 6.999995 v 8.54508 h -6.999995 z" />
      <circle
         style="fill:#000000;stroke-width:4.99996;stroke-linejoin:round"
         id="circle137"
         cx="94.966515"
         cy="139.89844"
         r="3"
         d="m 97.966515,139.89844 a 3,3 0 0 1 -3,3 3,3 0 0 1 -3,-3 3,3 0 0 1 3,-3 3,3 0 0 1 3,3 z" />
    </mask>
    <filter
       id="mask-powermask-path-effect139_inverse"
       inkscape:label="filtermask-powermask-path-effect139"
       style="color-interpolation-filters:sRGB"
       height="100"
       width="100"
       x="-50"
       y="-50">
      <feColorMatrix
         id="mask-powermask-path-effect139_primitive1"
         values="1"
         type="saturate"
         result="fbSourceGraphic" />
      <feColorMatrix
         id="mask-powermask-path-effect139_primitive2"
         values="-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 1 0 "
         in="fbSourceGraphic" />
    </filter>"""
	
"""<path
       style="fill:#be3075;stroke-width:4.99999;stroke-linejoin:round"
       id="path118"
       sodipodi:type="arc"
       sodipodi:cx="94.966515"
       sodipodi:cy="139.89844"
       sodipodi:rx="5"
       sodipodi:ry="5"
       sodipodi:start="4.712389"
       sodipodi:end="0.31415927"
       sodipodi:arc-type="slice"
       d="m 94.966515,134.89844 a 5,5 0 0 1 4.045085,2.06107 5,5 0 0 1 0.710197,4.48401 l -4.755282,-1.54508 z"
       mask="url(#mask-powermask-path-effect139)"
       inkscape:path-effect="#path-effect139" />"""

#What I actually get
"""<mask
maskUnits="userSpaceOnUse"
id="mask-powermask-path-effectgkCCAR">
<path
id="mask-powermask-path-effect145_box"
style="fill:#ffffff;fill-opacity:1"
d="m 91.966515,136.89844 h 5 v 5 h -5 z" />
<circle
style="fill:#000000;stroke:none;stroke-width:5;stroke-linejoin:round"
id="circle-mask-gkCCAR"
cx="94.966515"
cy="139.89844"
r="3"
d="m 97.966515,139.89844 a 3,3 0 0 1 -3,3 3,3 0 0 1 -3,-3 3,3 0 0 1 3,-3 3,3 0 0 1 3,3 z" />
</mask>
<filter
id="mask-powermask-path-effectgkCCAR_inverse"
inkscape:label="filtermask-powermask-path-effectgkCCAR"
style="color-interpolation-filters:sRGB"
height="100"
width="100"
x="-50"
y="-50">
<feColorMatrix
id="mask-powermask-path-effectgkCCAR_primitive1"
values="1"
type="saturate"
result="fbSourceGraphic" />
<feColorMatrix
id="mask-powermask-path-effectgkCCAR_primitive2"
values="-1 0 0 0 1 0 -1 0 0 1 0 0 -1 0 1 0 0 0 1 0 "
in="fbSourceGraphic" />
</filter>"""