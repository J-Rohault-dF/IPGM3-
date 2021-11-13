from copy import *
from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from ipgm.proportional import *
from twitterTextAdditions import *

from collectivites import *
from mapdrawer.mapper import *

allDivs = AllDivs('data/divs_us.txt')

partiesColors = {
	'Biden': Color('#3333FF'),
	'Trump': Color('#E81B23'),
	'Jorgensen': Color('#FED105'),
	'Hawkins': Color('#17aa5c'),

	'Nationalist': Color('#2e3147'),
	'Conservative': Color('#0365c0'),
	'Acela': Color('#f6af42'),
	'Labor': Color('#c82506'),
	'Green': Color('#00882b'),
}

#Get seats data
with open('data/seats_us.csv','r',encoding='utf8') as seatsDataFile:
	seatsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
	seatsData = {x[0]: {'seats': int(x[1]), 'layout': x[2], 'orientation': x[3], 'cx': toFloat(x[4]), 'cy': toFloat(x[5])} for x in seatsDataTemp[1:]}

seatsPerState = {k: v['seats'] for k,v in seatsData.items()}



#Party affiliation
#Biden Approval (?)
fV = loadDataTable('data/us_stats/2020_US_Vote.csv') #2020 vote
#Swing state (?)
#2020 Vote Method
rS = loadDataTable('data/us_stats/2019_US_Race.csv') #Race
#Age
#Education
#Income
#Employment
#Community
#Region
#Marital/Family (?)
#Religion
#Vaccination status

mx = importMatrices('data/pollDefs/us_parties.polld')

allExtrapolations = []
for i,j in [(fV, '2020_Parties'), (rS, '2019_Race')]:
	allExtrapolations.append(extrapolateResults(i, mx['Echelon']['matrix_{0}'.format(j)]))

rs = averageResultsSet(*allExtrapolations, allDivs=allDivs)

r = deepcopy(rs)
for i in ['West', 'Midwest', 'South', 'Northeast', 'National']:
	r = redressementResults(r, mx['Echelon']['scores_Parties'][i], allDivs=allDivs)

seatsParties = {x.name: proportionalHighestAverage(x, seatsPerState[x.name], 'D\'Hondt') for x in r.listOfResults if x.name in seatsPerState}

exportSeatsMap(r, seatsParties, seatsData, 'data/basemap_us_states.svg', 'redressed_us_Parties_Race.svg', allDivs=allDivs, partiesColors=partiesColors, scale=3)
