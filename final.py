### Project member Xinze Fan, Dezhou Chen

#### contribution :
#### Xinze Fan: Hypotheses 1 & 2
####			Function: def precipitation_ozone(filename),def yearRainAnanlyze(result),def watercover_ozone(yearfile),
####						def distance (x1,y1,x2,y2), def time_hours(t1,t2), def nearestSITE(vx,vy,number),def timeana(set,eruptime,start,end),
####						def ozone_vol(data,site,erupdate)
#### Dezhou Chen: Hypotheses 3 & 4
####			Function:

import os
import pandas as pd
from geographiclib.geodesic import Geodesic
import datetime
import time
import math
import matplotlib.pyplot as plt
import pylab as plt
########################
#### Xinze Fan #########
########################
def precipitation_ozone(filename):
	"""
	When there is a rain(PRECIPITATION ! = 0), analyze if the average ozone pollution in 3 hours after rain will be lower
	than the 3 hours before raining
	:param filename: given a year file name
	:return: for each siteID, the percentage that every time raining the ozone pollution tends to be lower
	>>> result = precipitation_ozone('data_used/ozone/metdata_2019.csv')
	>>> result['ABT147'] =  0.5214611872146119

	"""
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
				for i in range(0, 6):
					if (dex - i) > data.index[1]:
						before += data['OZONE'][dex - i]
						bc += 1
					if (dex + i) < data.index[-1]:
						after += data['OZONE'][dex + i]
						ac += 1
				if before!= 0 and after!=0:
					diff = (after / ac) - (before /bc)
					if diff < 0:
						better += 1
			result[data['SITE_ID'][ind]] = better/total
	return result
def yearRainAnanlyze(result):
	"""
	Analyze the year result, count the percentage that how many site getting better
	:param result: the previous result which have each site's better rate
	:return: the precentage that how many site getting better
	>>> result = precipitation_ozone('data_used/ozone/metdata_2010.csv')
	>>> print(yearRainAnanlyze(result))
	0.5357142857142857

	"""
	better = 0
	for re in result:
		if result[re] > 0.5:
			better += 1
	return better / len(result)

def watercover_ozone(yearfile):
	"""
	analyze state's ozone mean and match with the water coverage rater
	:param yearfile: metdata with year
	:return: a new dataframe which has state, ozone mean, coverage as column
	>>> result = watercover_ozone('data_used/ozone/metdata_2010.csv')
	>>> result[result['STATE'] == 'AZ']['OZONE']
	3    44.008963
	Name: OZONE, dtype: float64
	"""
	water = pd.read_csv('water_cover.csv', index_col=None, names=['STATE', 'COVERAGE'])
	for ind in water.index:
		num = water['COVERAGE'][ind]
		num = num.replace('%', '')
		num = float(num)
		water['COVERAGE'][ind] = num
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
    >>> distance(5.68, 7.95, 8.72, 20.81)
    788.006105005502
    >>> distance(10.25, 14.11, 18.82, 51.49)
    2229.96418603418
	>>> distance(16.708,145.780,41.84046,-72.010368)
	6724.862746550514
    """
    geod = Geodesic.WGS84
    dist = geod.Inverse(float(x1),float(y1),float(x2),float(y2))
    return  dist['s12'] /1852.0
def time_hours(t1,t2):
    """
    compute the time lag between two records
    :param t1: time 1
    :param t2: time 2
    :return: time lag in hours
    >>> time_hours('2010-05-29 00:00', '2010-05-28 23:00')
    -1.0
    """
    dt1 = datetime.datetime.strptime(str(t1),"%Y-%m-%d %H:%M")
    dt2 = datetime.datetime.strptime(str(t2),"%Y-%m-%d %H:%M")
    diff = (dt2-dt1).seconds/3600 + (dt2-dt1).days*24
    return diff
def nearestSITE(vx,vy,number):
	"""
	use distance functions to calculate the nearest SITE to the x,y
	:param vx: x of position that volcano erupted
	:param vy: y of position that volcano erupted
	:param number: number of nearest site
	:return: list of nearest SITE_ID
	>>> nearestSITE(16.708,145.780,5)
	{'HVT424': 3359.1784764667727, 'KVA428': 3715.4947252139095, 'DEN417': 3855.8991796178866, 'POF425': 3915.502661797372, 'OLY421': 4699.023392867393}
	"""
	resultSITE = {}
	loc = {}
	file = pd.read_csv('data_used/Site.csv')
	for ind in file.index:
		x2 =file['LATITUDE'][ind]
		y2 =file['LONGITUDE'][ind]
		loc[file['SITE_ID'][ind]] = distance(vx,vy,x2,y2)
	for i in range(0,number):
		min = 100000000000000
		ID = ""
		for item in loc:
			if min > loc[item]:
				min = loc[item]
				ID = item
		resultSITE[ID] = min
		del loc[ID]
	return resultSITE
def timeana(set,eruptime,start,end):
	"""
	according to the eruption time, return the ozone during the start and end time
	:param set: the dictionary of nearest site
	:param eruptime: the time of the volcano eruption
	:param start: plot start time
	:param end: plot end time
	:return: ozone pollution amount
	>>> data = pd.read_csv('data_used/ozone/metdata_2010.csv')
	>>> influ = data[data['SITE_ID'] == 'DEN417']
	>>> timeana(influ,'2010-05-29',-20,30)
	38.0
	"""
	eruptime = str(eruptime)+' 00:00'
	for ind in set.index:
		nt = str(set['DATE_TIME'][ind])[0:16]
		if (time_hours(eruptime,nt) < end) and (time_hours(eruptime,nt) >= start ) :
			return set['OZONE'][ind]

def ozone_vol(data,site,erupdate):
	"""
	ozone pollution and volcanoes analyze
	:param data: the metdata
	:param site: nearest site
	:param erupdate: erupt date
	:return: plot use to analyze
	"""
	# plot multiple lines with label, learnt from:https://stackoverflow.com/questions/11481644/how-do-i-assign-multiple-labels-at-once-in-matplotlib
	x = []
	y = []
	lab = []
	for si in site.keys():
		tx = []
		ty = []
		info = str(si) + ' ' + str(round(site[si])) + 'miles'
		lab.append(info)
		start = -48
		end = -42
		influ = data[data['SITE_ID'] == si]
		if not influ.empty:
			for i in range(0,30):
				start += 6
				end += 6
				tx.append(start)
				result = timeana(influ,erupdate,start,end)
				ty.append(result)
		x.append(tx)
		y.append(ty)

	for i in range(len(x)):
		if x[i] != [] and y[i] != []:
			plt.plot(x[i],y[i],label = lab[i]  )

	name = str(erupdate)
	plt.legend()
	plt.savefig('result/hypotheses2/'+ name+'.png')
	plt.clf()


###### main function:
if __name__ == "__main__":
	# Assumption1:
	# Does the rain fall affect the ozone pollution? Will the water coverage rate influence the ozone pollutions constancy?
	# Will the ozone pollutions tend to changed into wet-deposite with more rain fall?
	# ozone layer and deposition data : https://java.epa.gov/castnet/downloadprogress.do
	# water coverage data: https://www.usgs.gov/special-topic/water-science-school/science/how-wet-your-state-water-area-each-state?qt-science_center_objects=0#qt-science_center_objects
	# 2019 example
	water = pd.read_csv('water_cover.csv', index_col=None, names=['STATE', 'COVERAGE'])
	for ind in water.index:
		num = water['COVERAGE'][ind]
		num = num.replace('%', '')
		num = float(num)
		water['COVERAGE'][ind] = num
	result = precipitation_ozone('data_used/ozone/metdata_2019.csv')
	print(yearRainAnanlyze(result))
	# 10 years result
	for i in range(10,20):
		file = 'data_used/ozone/metdata_20' + str(i) +'.csv'
		result = precipitation_ozone(file)
		print('year: ',i)
		print(yearRainAnanlyze(result))

	# ozone pollution change with water coverage
	for i in range(10,20):
		file = 'data_used/ozone/metdata_20' + str(i)+'.csv'
		result = watercover_ozone(file)

		# plot package used on https://matplotlib.org/tutorials/introductory/pyplot.html
		plt.plot(result['COVERAGE'],result['OZONE'])
	plt.savefig('result/hypotheses1/watercover_ozone.png')

	# ozone plution changing rate each year :
	state_ozone = {}
	calcul = {}
	for ind in water.index:
		if water['STATE'][ind] not in state_ozone:
			state_ozone[water['STATE'][ind]] = 0
			calcul[water['STATE'][ind]] = []
	for i in range(10, 20):
		before = 0
		file = 'data_used/ozone/metdata_20' + str(i) + '.csv'

		result = watercover_ozone( file)
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
	plt.savefig('result/hypotheses1/watercover_growRate.png')
### Assumption 2 : volcanos influence
# volcanoes dataset from :https://www.ngdc.noaa.gov/hazel/view/hazards/volcano/event-data?maxYear=2020&minYear=2010&country=United%20States
# read in volcanos data
	volcano = pd.read_csv('data_used/volcanos.csv')
# focus on the eruption date,year and the nearest 5 site.
	for ind in volcano.index:
		errupDate = str(volcano['Date'][ind])
		year = errupDate[0:4]
		file = 'data_used/ozone/metdata_' + str(year) + '.csv'
		file = pd.read_csv(file)
		file = file[file['OZONE'].notna()]
		vx = volcano['Latitude'][ind]
		vy = volcano['Longitude'][ind]
		site = nearestSITE(vx,vy,5)
		ozone_vol(file,site,errupDate)
################################
###### Dezhou Chen  ############
################################





