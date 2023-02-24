import os
from copy import *

from ipgm.utils import *
from ipgm.port import *
from ipgm.mainFuncs import *
from twitterTextAdditions import *
from divsHandler import *
from mapdrawer.mapper import *

#Get divs data
#with open('data/nl/rings/provinces.csv','r',encoding='utf8') as seatsDataFile:
#	ringsDataTemp = [y.split(';') for y in [x for x in seatsDataFile.read().split('\n')]]
#	ringsData = {x[0]: dict(zip(ringsDataTemp[0][1:], [toFloatOrStr(y) for y in x[1:]])) for x in ringsDataTemp[1:]}

allDivs = AllDivs('data/nl/divs/nl_2002-.txt')


candidaciesData: Candidacies = importCandidacies(src='data/nl/cands/parties.csv')
parties = [x.shortName for x in candidaciesData.listOfCands]

#Note: Vianen was in Zuid-Holland until 2002-01-01

#tk_2021 = importDataTable('data/nl/stats/2021TK.csv', allDivs)
#tk_2017 = importDataTable('data/nl/stats/TK20170315.csv', allDivs)
#ep_2019 = importDataTable('data/nl/stats/2019EP.csv', allDivs)
#ps_2019 = importDataTable('data/nl/stats/2019PS.csv', allDivs)
list_elections = [(importDataTable('data/nl/stats/'+election+'.csv', allDivs), election) for election in [
#	'TK20210317',
	'TK20170315',
#	'TK20120912',
#	'TK20100609',
#	'TK20061122',
#	'TK20030122',
#	'TK20020515',
#	'TK19980506',
#	'TK19940503',
#	'TK19890906',
#	'TK19860521',
#	'TK19820908',
#	'TK19810526',
#	'TK19770525',
#	'TK19721129',
#	'TK19710428',
#	'TK19670215',
#	'TK19630515',
#	'TK19590312',
#	'TK19560613',
#	'TK19520625',
#	'TK19480707',
#	'TK19460517',
#	'TK19370526',
#	'TK19330426',
#	'TK19290703',
#	'TK19250701',
#	'TK19220705',
#	'TK19180702',
#	'EP19790607',
#	'EP19840614',
#	'EP19890615',
#	'EP19940609',
#	'EP19990610',
#	'EP20040610',
#	'EP20090604',
#	'EP20140522',
#	'EP20190523',
#	'PS19310422',
#	'PS19350417',
#	'PS19390419',
#	'PS19460529',
#	'PS19500426',
#	'PS19540421',
#	'PS19580326',
#	'PS19620328',
#	'PS19660323',
#	'PS19700318',
#	'PS19740327',
#	'PS19780329',
#	'PS19820324',
#	'PS19870318',
#	'PS19910306',
#	'PS19950308',
#	'PS19990303',
#	'PS20030311',
#	'PS20070307',
#	'PS20110302',
#	'PS20150318',
#	'PS20190320',
]]

for election, name in list_elections:
	print(name)
	exportMap(election, 'data/nl/maps/provinces.svg', 'nl/'+name+'_p.svg', candidaciesData=candidaciesData)
	exportMap(election, 'data/nl/maps/gemeenten_'+name[2:6]+'.svg', 'nl/'+name+'_g.svg', candidaciesData=candidaciesData)
	print(election)