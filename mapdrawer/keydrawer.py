from mapdrawer.colors import *

#Useful functions:
#Draw rectangle of a color
def drawRectangle(x0: float, y0: float, width: float, height: float, fill: Color, id: str) -> str:
	return '<rect style="fill:{fill};stroke:none;stroke-width:0;stroke-linejoin:round" id="rect-{id}" width="{width}" height="{height}" x="{x0}" y="{y0}" />'.format(fill=fill, id=id, width=width, height=height, x0=x0, y0=y0)

#(find highest used id in svg)

#Draw bars

#Write text
def drawText(text: str, x0: float, y0: float, fontSize: float, align: str, id: str) -> str:
	return '''<text
style="font-size:{fontSize}px;line-height:1;font-family:Ubuntu;stroke-width:0;text-anchor:{align};text-align:{align};"
x="{x0}"
y="{y0}"
id="text-{id}"><tspan
id="textspan-{id}"
x="33.141422"
y="{y0}"
style="stroke-width:0;text-anchor:{align};text-align:{align};">{text}</tspan></text>'''.format(align=align, fontSize=fontSize, x0=x0, y0=y0, id=id, text=text)

#Write percentages legend

#Draw whole candidate bar
def drawCandidate(name: str, score: float):
	#Write name
	#Draw bar with percentage
	#Put key boxes
	pass