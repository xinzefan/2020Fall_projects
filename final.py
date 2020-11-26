import os

import pandas as pd
from geographiclib.geodesic import Geodesic
import datetime
import time
import math
import matplotlib.pyplot as plt
# Assumption 1 : Is the area with more water coverage has a less change in the amount of ozone layer?
#				 If it is, how much its changed in percentage less than other area?
#				 When there are more raining, is the situation better than before?
# Assumption 2 : Is the volcano's eruption  influenced the ozone layer? if so, how much it was influcened?
#
# Assumption 3 : Is there a periodic term in changing? Like summer and winter the pollution terns to be more.

# Assumption1:
# ozone layer and deposition data : https://java.epa.gov/castnet/downloadprogress.do
# water coverage data: https://www.usgs.gov/special-topic/water-science-school/science/how-wet-your-state-water-area-each-state?qt-science_center_objects=0#qt-science_center_objects
def precipitation_ozone(filename):
	data = pd.read_csv(filename)
	data = data.sort_values(by=['SITE_ID','DATE_TIME'])
	result = {}
	for ind in data.index:
		if data['SITE_ID'][ind] not in result:
			#result[data['SITE_ID'][ind]] = {}
			temp = data[data['SITE_ID']==data['SITE_ID'][ind]]
			rain = temp[temp['PRECIPITATION'] != 0.0]
			total = 0
			better = 0
			for dex in rain.index:
				total +=1
				before = 0
				bc = 1
				after = 0
				ac = 1
				for i in range(0, 4):
					if (dex - i) > data.index[1]:
						before += data['OZONE'][dex - i]
						bc += 1
					if (dex + i) < data.index[-1]:
						after += data['OZONE'][dex + i]
						ac += 1
				if before!= 0 and after!=0:
					percentc = (after / ac) / (before /bc)
					if percentc > 1:
						better += 1
			result[data['SITE_ID'][ind]] = better/total
	return result

def watercover_ozone(water,yearfile):
	ozoneyear = pd.read_csv(yearfile)
	site_state = pd.read_csv('Site.csv')
	temp = ozoneyear.groupby(['SITE_ID']).mean()
	data = temp['OZONE']
	result = site_state.merge(data,left_on='SITE_ID',right_on='SITE_ID')[['SITE_ID','STATE','OZONE']]
	result = result.dropna()
	result = result.groupby(['STATE']).mean()
	result = result.merge(water,left_on='STATE',right_on='STATE')
	result = result.sort_values(['COVERAGE'])
	return  result

###Assumption2 : volcanos data from: https://www.ngdc.noaa.gov/hazel/view/hazards/volcano/event-data?maxYear=2020&minYear=2000&country=United%20States
def distance (x1,y1,x2,y2):
    """
    give the two position, return in miles
    :param x1: first position x
    :param y1: first position y
    :param x2: second position x
    :param y2: second position y
    :return: miles in float
    """
    geod = Geodesic.WGS84
    dist = geod.Inverse(float(x1),float(y1),float(x2),float(y2))
    return  dist['s12'] /1852.0
###### main function:
if __name__ == "__main__":
	#result = precipitation_ozone('ozone/metdata_2019.csv')
	#print(result)
### Assumption1 :
	water = pd.read_csv('water_cover.csv', index_col=None, names=['STATE', 'COVERAGE'])
	for ind in water.index:
		num = water['COVERAGE'][ind]
		num = num.replace('%', '')
		num = float(num)
		water['COVERAGE'][ind] = num
	# ozone polution change with water coverage
	"""for i in range(10,20):
		file = 'ozone/metdata_20' + str(i)+'.csv'
		result = watercover_ozone(water,file)
		# plot package used on https://matplotlib.org/tutorials/introductory/pyplot.html
		plt.plot(result['COVERAGE'],result['OZONE'])
	plt.savefig('watercover_ozone.png')

	# ozone plution changing rate each year :
	state_ozone = {}
	calcul = {}
	for ind in water.index:
		if water['STATE'][ind] not in state_ozone:
			state_ozone[water['STATE'][ind]] = 0
			calcul[water['STATE'][ind]] = []
	for i in range(10, 20):
		before = 0
		file = 'ozone/metdata_20' + str(i) + '.csv'
		result = watercover_ozone(water, file)
		for ind in result.index:
			calcul[result['STATE'][ind]].append(result['OZONE'][ind])
	for re in calcul:
		if len(calcul[re]) != 0:
			lst = []
			current = calcul[re][0]
			for item in calcul[re][1:]:
				if current != 0 and item !=0:
					lst.append((item-current)/current)
			sum = 0
			for item in lst:
				sum += item
			final = sum/len(lst)
			state_ozone[re] = final
	### plot
	x = []
	y = []
	for ind in result.index:
		x.append(result['COVERAGE'][ind])
		y.append(state_ozone[result['STATE'][ind]])
	plt.plot(x,y)
	plt.savefig('watercover_growRate.png')"""
### Assumption 2 : volcanos influence

	#volcano = pd.read_csv('volcanos.csv')
	#print(volcano)