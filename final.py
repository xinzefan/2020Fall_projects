import os

import pandas as pd
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

###### main function:
if __name__ == "__main__":
	#result = precipitation_ozone('ozone/metdata_2019.csv')
	#print(result)
### water coverage
	water = pd.read_csv('water_cover.csv', index_col=None, names=['STATE', 'COVERAGE'])
	for ind in water.index:
		num = water['COVERAGE'][ind]
		num = num.replace('%', '')
		num = float(num)
		water['COVERAGE'][ind] = num
	for i in range(10,20):
		file = 'ozone/metdata_20' + str(i)+'.csv'
		result = watercover_ozone(water,file)
# plot package used on https://matplotlib.org/tutorials/introductory/pyplot.html
		plt.plot(result['COVERAGE'],result['OZONE'])
	plt.show()
	#volcano = pd.read_csv('volcanos.csv')
	#print(volcano)