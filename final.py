### Project member Xinze Fan, Dezhou Chen

#### contribution :
#### Xinze Fan: Hypotheses 1 & 2
####			Function: def precipitation_ozone(filename),def yearRainAnanlyze(result),def watercover_ozone(yearfile),
####						def distance (x1,y1,x2,y2), def time_hours(t1,t2), def nearestSITE(vx,vy,number),def timeana(set,eruptime,start,end),
####						def ozone_vol(data,site,erupdate)，def ozone_region(meta,site,state_region,year)
#### Dezhou Chen: Hypotheses 3 & 4
####			Function:	def month_ozone(year,site)，def ozone_region(meta,site,state_region,year)

import os
import pandas as pd
from geographiclib.geodesic import Geodesic
import datetime
import time
import math
import matplotlib.pyplot as plt
import pylab as plt
import numpy as np
import statistics
from matplotlib import pyplot as plt
from math import sqrt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

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

######### Dezhou Chen  ######
#Citation: https://www.youtube.com/watch?v=3aOtG9ns_Ko&feature=youtu.be
#coverting structure and using month structure
#Citation:https://stackoverflow.com/questions/46789098/create-new-column-in-dataframe-with-match-values-from-other-dataframe
#using strucutre of mapping
def month_ozone(year,site):
	"""
	Boxplot for months and ozone mean for each year and dataframe statistics result
	:param year: input year for each year between 2015 and 2019
	:param site: read Site.csv file and assign as site
	:return: rebased data
	>>> sit = pd.read_csv('data_used/Site.csv')
	>>> site = sit[['SITE_ID', 'STATE']]
	>>> test = month_ozone(15,site)
	>>> test.loc[(test['STATE']=='AK')& ( test['MONTH'] == 1)]['OZONE']
	0    35.848118
	Name: OZONE, dtype: float64
	"""
	file = "data_used/ozone/metdata_20" + str(year) + ".csv"
	data = pd.read_csv(file)
	data = data[['SITE_ID', 'DATE_TIME', 'OZONE']]
	data['DATE_TIME'] = pd.to_datetime(data['DATE_TIME'])
	data['MONTH'] = data['DATE_TIME'].dt.month
	data['STATE'] = data['SITE_ID'].map(site.set_index('SITE_ID')['STATE'])
	data = data.groupby(["STATE", "MONTH"]).mean().reset_index()
	plt.figure()
	nr = sns.boxplot(x='MONTH', y = "OZONE", data = data)
	nr.set_title('Year 20' + str(year))
	path = 'result/hypotheses3/'+str(year)
	plt.savefig(path +'.png')
	return data
def ozone_region(meta,site,state_region,year):
	"""
	 dataframe between regions and ozone mean in each specific year from 2015 - 2019
	:param meta: meta dataframe for each year between 2015 and 2019
	:param site: read Site.csv file and assign as site
	:param state_region: read state_region file for state corresponding with region and assign as state_region
	:param year: input year for each year between 2015 and 2019
	:return: dataframe between each region and ozone mean in specific year
	>>> tem = pd.read_csv('data_used/ozone/metdata_2015.csv')
	>>> sit = pd.read_csv('data_used/Site.csv')
	>>> reg = pd.read_csv('data_used/state_region.csv')
	>>> test = ozone_region(tem,sit,reg,2015)
	>>> test[test['REGION'] == 'Midwest']['OZONE_MEAN_2015']
	0    29.4
	Name: OZONE_MEAN_2015, dtype: float64
	"""
	meta = meta[['SITE_ID', 'OZONE']]
	result = pd.concat([meta, site], axis=1, sort=False)
	result = result.groupby("STATE").mean()
	result = result.reset_index()
	diff = result.columns.difference(state_region.columns)
	dataframe = pd.merge(state_region, result[diff], left_index=True, right_index=True, how='outer')
	dataframe = dataframe.sort_values(by=['REGION'])
	dataframe = dataframe[['REGION', 'OZONE']]
	dataframe = dataframe.groupby("REGION").mean().round(1)
	dataframe= dataframe.reset_index()
	newname = 'OZONE_MEAN_' + str(year)
	dataframe.columns = ['REGION', newname]
	return dataframe

###### main function:
if __name__ == "__main__":
	# Hypothesis1:
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
### Hypothesis 2 : volcanos influence
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
#########
	state_region = pd.read_csv("data_used/state_region.csv")
	site = pd.read_csv("data_used/Site.csv")
###### Hypothesis 3
	site = site[['SITE_ID', 'STATE']]
	first = month_ozone(15,site)
	first = first.groupby(["MONTH"]).mean().reset_index()
	for i in range(16, 20):
		result = month_ozone(i, site)
		result = result.groupby(["MONTH"]).mean().reset_index()
		first = pd.concat([first, result]).groupby('MONTH', as_index=False).mean()
	first = first.rename(columns={'OZONE': 'OZONE_MEAN_TOTAL'})
	print(first)
	### result for all years
	fig = px.bar(first, x='MONTH', y='OZONE_MEAN_TOTAL')
	fig.write_image('result/hypotheses3/allyear.png')
##### hypothesis 4
#Citation:
#https://stackoverflow.com/questions/14940743/selecting-excluding-sets-of-columns-in-pandas
#usage of difference() structure
	r1 = pd.read_csv('data_used/ozone/metdata_2015.csv')
	r1 = ozone_region(r1,site,state_region,15)
	for i in range(15, 20):
		file = 'data_used/ozone/metdata_20' + str(i) + '.csv'
		meta = pd.read_csv(file)
		#site = site[['SITE_ID', 'STATE']]
		resultframe = ozone_region(meta,site,state_region,i)
		r1 = r1.merge(resultframe, how='outer')
	r1['OZONE_MEAN_TOTAL'] = r1[['OZONE_MEAN_15', 'OZONE_MEAN_16', 'OZONE_MEAN_17', 'OZONE_MEAN_18', 'OZONE_MEAN_19']].mean(axis=1)
	#### plot
	# plotting for hypothesis4
	# Citation:https://plotly.com/python/bar-charts/
	# using the strucutre of go.Figure
	regions = ['Midwest', 'Northeast', 'South', 'West']
	fig = go.Figure(data=[
		go.Bar(name='Year2015', x=regions, y=[30.4, 25.1, 29.7, 29.1]),
		go.Bar(name='Year2016', x=regions, y=[26.0, 23.8, 29.9, 29.0]),
		go.Bar(name='Year2017', x=regions, y=[30.0, 30.3, 29.0, 29.6]),
		go.Bar(name='Year2018', x=regions, y=[33.7, 34.1, 33.5, 32.1]),
		go.Bar(name='Year2019', x=regions, y=[26.1, 28.8, 25.3, 23.6]),
	])
	fig.update_layout(barmode='group', title="Multiple Year Comparison Between Region And Ozone Mean ",
					  xaxis_title="REGION", yaxis_title="OZONE MEAN")
	fig.write_image('result/hypotheses4/multiyear.png')

	r1 = r1.sort_values(by=['OZONE_MEAN_TOTAL'], ascending=False)
	fig = px.bar(r1, x='REGION', y='OZONE_MEAN_TOTAL')
	fig.write_image('result/hypotheses4/region_year.png')




