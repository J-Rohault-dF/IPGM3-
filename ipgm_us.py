from copy import *
from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from ipgm.additions import *

from collectivites import *
from mapdrawer.mapper import *

allDivs = AllDivs('divs_us.txt')

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

#Party affiliation
#Biden Approval (?)
fV = loadDataTable('us_stats/2020_US_Vote.csv') #2020 vote
#Swing state (?)
#2020 Vote Method
rS = loadDataTable('us_stats/2019_US_Race.csv')#Race
#Age
#Education
#Income
#Employment
#Community
#Region
#Marital/Family (?)
#Religion
#Vaccination status

mx = importMatrices('us_parties.polld')

allExtrapolations = []
for i,j in [(fV, '2020_Parties'), (rS, '2019_Race')]:
	allExtrapolations.append(extrapolateResults(i, mx['components_Echelon_{0}'.format(j)]))

r = averageResultsSet(*allExtrapolations, allDivs=allDivs)

rs = deepcopy(r)
for i in ['West', 'Midwest', 'South', 'Northeast', 'National']:
	rs = redressementResults(rs, mx['scores_Echelon_Parties'][i], allDivs=allDivs)

exportMap(rs, 'basemap_us_states.svg', 'redressed_us_Parties_Race.svg', allDivs=allDivs, partiesColors=partiesColors)