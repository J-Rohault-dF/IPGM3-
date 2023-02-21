from divsHandler import *
from ipgm.port import *
from mapdrawer.mapper import *


allDivs = AllDivs('data/zh/divs/zh.txt')

#t = importDataTable('data/zh/stats/KR07.csv', allDivs)

#KR07 (wkr)
#with open('data/zh/stats/KR07.csv', 'r') as dat:
#	res = [[x.split(';')[0], x.split(';')[1], float(x.split(';')[2])] for x in dat.read().split('\n')]
#candidaciesData = importCandidacies('data/zh/cands/parties.csv')
#mapColorerExporterRaw(res, candidaciesData, 'data/zh/maps/zh_wkr.svg', 'zh/test__.svg')

#RGR07 (gmd)
#with open('data/zh/stats/RGR07.csv', 'r') as dat:
#	res = [[x.split(';')[0], x.split(';')[1], float(x.split(';')[2])] for x in dat.read().split('\n')]
#candidaciesData = importCandidacies('data/zh/cands/cands_zh07.csv')
#mapColorerExporterRaw(res, candidaciesData, 'data/zh/maps/zh_gmd_w_s.svg', 'zh/rgr07_gmd.svg')

#RGR07-elected
#with open('data/zh/stats/RGR07-elected.csv', 'r') as dat:
#	res = [[x.split(';')[0], x.split(';')[1][1:-3]] for x in dat.read().split('\n')]
#candidaciesData = importCandidacies('data/zh/cands/cands_zh07-elected.csv')
#mapColorerExporterStraight(res, candidaciesData, 'data/zh/maps/zh_gmd_w_s.svg', 'zh/rgr07_gmd_elected.svg')

#RGR11 (gmd)
with open('data/zh/stats/RGR11.csv', 'r') as dat:
	res = [[x.split(';')[0], x.split(';')[1], float(x.split(';')[2])] for x in dat.read().split('\n')]
candidaciesData = importCandidacies('data/zh/cands/cands_zh11.csv')
mapColorerExporterRaw(res, candidaciesData, 'data/zh/maps/zh_gmd_w_s.svg', 'zh/rgr11_gmd.svg')
