# 2020Fall_projects
# Team member & Contributes: 
   Xinze Fan, Dezhou Chen   
#Topic: 
   Ozone layer/ Ozone pollution or related gas analyze.
#Backgroud Information:

# Assumption 1:  
- Data Used:      
    - metdata_year.csv in ozone folder which contains the precipitation and ozone data for all the sites in united states.    
    - Site.csv : pair each SITE_ID to which State it actually in.     
    - water_cover.csv : each States' water coverage rate in United States.
- Dose the rain falls influence the ozone pollution?    
    (People always feel the air is more fresh and clean after raining. So is that means when it is raining, the water will have some chemical reaction with the ozone pollution. If this is true, it means after raining, the ozone pollution amount will smaller.)       

    We calculate the 5 hours average ozone pollution before each raining, and also the 5 hours average ozone pollution after each time of raining.
    Then we calculate the rate which the times that pollution is getting lower divided by the total times of raining.
    Below are the 10 example result by the SiteID in alphabetical order.
          
   SITE_ID  rate of getting better   
    ABT147  0.5108447488584474      
    ACA416  0.4541176470588235      
    ALC188  0.5356164383561643     
    ALH157  0.5323059360730593     
    ANA115  0.5202054794520548     
    ARE128  0.541324200913242     
    ASH135  0.5256849315068494      
    BAS601  0.40764331210191085     
    BBE401  0.3       
    BEL116  0.5787545787545788     
    BFT142  0.39509132420091325      
         
    As a overview for all United States in year 2010-2019:    
    we have the highest rate: 0.6363636363636364 and the lowest rate: 0.47619047619047616
    
    2010: 0.5357142857142857    
    2011: 0.47619047619047616   
    2012: 0.5934065934065934   
    2013: 0.5869565217391305     
    2014: 0.6     
    2015: 0.5876288659793815   
    2016: 0.53125     
    2017: 0.5833333333333334      
    2018: 0.5773195876288659   
    2019: 0.6363636363636364     
    
    Through the data above, we can see that only 1 year has less than 50% of the better SITE.     
   
    ---- Conclusion ----    
    The rain fall (PRECIPITATION) has significant influence on the ozone pollution. The recent 10 years data shows that around 60% of the site's pollution each year will be optimized by the rain.    
- How is the water coverage influence the ozone pollution?     
    (From the previous analyze, we found that water does influence the ozone pollution. So after analyzed the water from rain fall, we want to focus on the other side: the water in the lake or river.   
     We want to see if the water coverage of each state affect to the ozone pollution.)
     
    Below is plot shows the relationship between the state water coverage with the average ozone pollution.    
    The x-axis is the percentage of the state water coverage rate, the y-axis is the mean ozone pollution for that state. And each line represent a single year. So the plot show the recent 10 years, each state's water coverage with the mean ozone pollution.   
    ![diagram](result_graph/water/watercover_ozone.png)   
    From the plot, we can see that the coverage of the 0-10% has huge difference in each states so that the lines are tend to be more bounce.
    The coverage rate 10-20% is much more flat. And the lines going aggregation at the end. Of course since there are not too much states have the water coverage rate in 30-40%, it is not a significant value to give the conclusion that the line are going aggregation. However, we have a significant amount of states are in the 10-20% range. From this part
    we can prove that with the higher water coverage, the ozone pollutions are tend to be more flat curve and they aggregated to a certain range. 
    
    Further more, we also analyzed the ozone pollution growth rate. Consider about how CO2's circulation in the earth, water is an important part to do the chemical reaction and a buffer. So if our assumption is correct, as how CO2 circulation, the ozone pollution should have less changing rate in the area with more water coverage.   
    ![diagram](result_graph/water/watercover_growRate.png)    
    This plot shows the relationship between the water coverage and the growth rate of the ozone pollution in recent 10 years. (x-axis: the water coverage, y-axis: recent 10 years average ozone growth rate)       
    From the plot we can indicate that same as the previous analyze, the more water a state has, it has a more constant growth rate. 0-5% water coverage part have a really bouncy line which we believe that since there is too little water to reaction with ozone-pollution and has almost no buffer to the rapidly increasing ozone pollution. 
    And the area with 5% - 20% are tend to be converge in growth rate -10% - 0%. Such analyze proved that our previous assumption is correct.     
    ---- Conclusion ----    
    The water act as a buffer in the ozone circulation, so with the higher water coverage, the ozone pollution's mean are tend to be more converge. And if a state has a higher water coverage, its ozone pollution's growth rate is less likely to change either.
     
    
# Assumption 2:
Assumption2:     
Will the volcanoes eruption influence the ozone polution?
How about other pollution gas changing? 