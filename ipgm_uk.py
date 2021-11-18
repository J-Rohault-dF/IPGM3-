from copy import *

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from collectivites import *
from mapdrawer.mapper import *

partiesColors = { #Should put the actual colors
	'Conservative': Color('#0087DC'),
	'Labour': Color('#E4003B'),
	'Liberal Democrats': Color('#FAA61A'),
	'Green': Color('#00ff00'),
	'Brexit': Color('#ff00ff'),
	'SNP': Color('#FDF38E'),
	'Plaid Cymru': Color('#005B54'),
	'Others': Color('#000000'),

	'Boris Johnson': Color('#0087DC'),
	'Rishi Sunak': Color('#4e42f5'),
	'Keir Starmer': Color('#E4003B'),
	'Andy Burnham': Color('#E4003B'),
	'Sadiq Khan': Color('#E4003B'),
	'Angela Rayner': Color('#E4003B'),
}

allDivs = AllDivs('data/divs_uk.txt')

t = loadDataTable('data/uk_stats/2019GE.csv')

mx = importMatricesJson('data/pollDefs/uk/R&WS_20211115.json')
sampleSize = mx.pop('sampleSize')

doExportTxt = True
doExportMap = True
doExportCsv = True



allTexts = []

for hk, hv in mx.items():
	tn = int(hk[0])

	if tn == 1:
		r = extrapolateResults(t, hv['matrix_{h}'.format(h=hk)])
		r1 = deepcopy(r)
	else:
		r = extrapolateResults(r1, hv['matrix_{h}'.format(h=hk)])

	curScores = hv[('scores_{h}'.format(h=hk))]
	for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
		r = redressementResults(r, curScores[i], allDivs=allDivs)
	
	#for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
	#	showRes(r.get(i, allDivs))

	#Tweet text
	if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.get('Great Britain', allDivs=allDivs).toPercentages(), sampleSize, top=1, nbSimulated=15000))

	#Export and map
	if doExportCsv: saveDataTable('exports/{h}.csv'.format(h=hk), r)
	if doExportMap: exportMap(r, 'data/basemap_gb_counties_merged.svg', '{h}.svg'.format(h=hk), allDivs=allDivs, partiesColors=partiesColors)
	#if doExportMap: exportMap(r, 'data/basemap_depts.svg', '{h}.svg'.format(h=hk), allDivs=allDivs, partiesColors=partiesColors)

if doExportTxt:
	with open('exports/tweetText.txt','w',encoding='utf8') as txtFile:
		txtFile.write('\n\n'.join(allTexts))

