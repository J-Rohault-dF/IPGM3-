from colour import *

finalText = ''

partiesColors = {
	'FaE': Color('#990f4b'),
	'SA': Color('#5BB286'),
	'LWP': Color('#c6080b'),
	'Rbw': Color('#ff66c4'),
	'DL': Color('#0f7606'),
	'CP': Color('#ee2e3c'),
	'3P': Color('#75D155'),
	'Volt': Color('#7c17bf'),
	'V+H': Color('#7c17bf'),
	'V_H': Color('#7c17bf'),
	'': Color('#fff'),
	'LP': Color('#ffc022'),
	'UsN': Color('#004080'),
	'CU': Color('#396ccc'),
	'Lbt': Color('#c9a726'),
	'PLUS': Color('#ba852e'),
	'ILA': Color('#55a45a'),
	'DXT': Color('#0CB4D4'),
	'NCU': Color('#1C0054'),
	'G21': Color('#2cb517'),
	'HC': Color('#ff5900'),
	'IDP': Color('#10275b'),
	'AGP': Color('#e3891d'),
	'THF': Color('#a9eed1'),
	'Ref': Color('#55a45a'),
	'PFP': Color('#7c17bf'),
	'ASU_DFS': Color('#cfb997'),
	'Cent': Color('#cfb997'),
	'ERA': Color('#4F5951'),
	'NR': Color('#710099'),
}

#Get the text
with open('toConvert.txt','r',encoding='utf8') as toConvert:
	for line in toConvert:
		if 'HexShade/cell' in line:
			templateCall = line.split('{{')[1].split('}}')[0]
			party = templateCall.split('|')[1]
			lum = templateCall.split('|')[2]

			if party in partiesColors.keys(): c = partiesColors[party]
			else:
				print('Color missing: {p}'.format(p=party))
				c = Color('#fff')
			c.set_luminance(lum)

			finalText += line.replace(('{{'+templateCall+'}}'), 'style="background-color:{c}"'.format(c=c.get_hex_l()))


		else: finalText += line

with open('converted.txt','w',encoding='utf8') as converted:
	converted.write(finalText)