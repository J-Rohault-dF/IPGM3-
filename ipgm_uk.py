from copy import *

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from ipgm.proportional import *
from twitterTextAdditions import *
from collectivites import *
from mapdrawer.mapper import *

partiesColors = { #Should put the actual colors
	'Conservative': Color('#0087DC'),
	'Labour': Color('#E4003B'),
	'Liberal Democrats': Color('#FAA61A'),
	'Green': Color('#6AB023'),
	'SNP': Color('#FDF38E'),
	'Plaid Cymru': Color('#005B54'),
	'Brexit': Color('#12B6CF'),
	'Reform': Color('#12B6CF'),
	'Others': Color('#000000'),

	'Boris Johnson': Color('#0087DC'),
	'Rishi Sunak': Color('#4e42f5'),
	'Keir Starmer': Color('#E4003B'),
	'Andy Burnham': Color('#E4003B'),
	'Sadiq Khan': Color('#E4003B'),
	'Angela Rayner': Color('#E4003B'),
}


#Get seats data
with open('data/seats_uk.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsData = {x[0]: {'seats': int(x[1]), 'layout': x[2], 'orientation': x[3], 'cx': toFloat(x[4]), 'cy': toFloat(x[5])} for x in seatsDataTemp[1:]}

seatsPerRegion = {k: v['seats'] for k,v in seatsData.items()}




allDivs = AllDivs('data/divs_uk.txt')

t = loadDataTable('data/uk_stats/2019GE.csv')

poll = 'uk/RaWS_20211121'

mx = importMatricesJson('data/pollDefs/{0}.json'.format(poll))
if not os.path.exists('exports/{path}'.format(path=poll)):
	os.makedirs('exports/{path}'.format(path=poll))

doExportTxt = True
doExportMap = False
doExportCsv = True

doExportPropMap = False

allRounds = {}
allSeats = {}
allTexts = []

for hk, hv in {k: v for k,v in mx.items() if k != 'sampleSize'}.items():
	tn = int(hk[0])

	if tn == 1:
		r = extrapolateResults(t, hv['matrix_2019GE_2024GE'.format(h=hk)])
		r1 = deepcopy(r)
	else:
		r = extrapolateResults(r1, hv['matrix_2019GE_2024R2'.format(h=hk)])

	curScores = hv[('scores_2024{0}'.format('GE' if tn == 1 else 'R2').format(h=hk))]
	for i in sorted(curScores, key=lambda x: allDivs.getSortingKeys(x)):
		r = redressementResults(r, curScores[i], allDivs=allDivs, weight=(1 if i == 'Great Britain' else 0.5))
	
	seatsParties = {x: proportionalHighestAverage(filterThreshold(r.get(x, allDivs), 0.05), seatsPerRegion[x], 'D\'Hondt') for x in allDivs.allDivs if x in seatsPerRegion}
	
	#Put it in allRounds
	allRounds[hk] = r
	allSeats[hk] = seatsParties
	
	#Tweet text
	if doExportTxt: allTexts.append('HYPOTHESIS {h}\n'.format(h=hk)+makeTweetText(r.get('Great Britain', allDivs=allDivs).toPercentages(), hv['sampleSize'], top=1, nbSimulated=15000))

	#Export and map
	if doExportCsv: saveDataTable('exports/{path}/{h}.csv'.format(h=hk, path=poll), r)
	if doExportMap:
		exportMap(r, 'data/basemap_gb_counties_merged.svg', '{path}/{h}.svg'.format(h=hk, path=poll), allDivs=allDivs, partiesColors=partiesColors)
	if doExportPropMap and tn == 1:
		exportSeatsMap(r, seatsParties, seatsData, 'data/basemap_gb_regions.svg', '{path}/{h}_prop.svg'.format(h=hk, path=poll), allDivs=allDivs, partiesColors=partiesColors, scale=0.6)


if doExportTxt:
	with open('exports/{path}/tweetText.txt'.format(path=poll),'w',encoding='utf8') as txtFile:
		txtFile.write('\n\n'.join(allTexts))

