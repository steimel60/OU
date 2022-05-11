reset;
option solver cplex;
option cplex_options 'sensitivity';

#---------------------------Sets-------------------------------------
set LOT_TYPE;	#New lot options

#------------------------Parameters----------------------------------

param acres {LOT_TYPE} >= 0;			#Acres required for lot type
param cost {LOT_TYPE} >= 0;			#Cost of building new lot type
param profit {LOT_TYPE} >= 0;		#Expected profit from new lot type
param min_percent {LOT_TYPE} >= 0;	#Percent of all lots for each type
param budget = 15000000;			#Federal Grant Budget


#-------------------------Decision Variables---------------------------

var DEMO integer >= 0;				#Number of lots to demolish
var COUNT {LOT_TYPE} integer >= 0;	#Number of lots to build for each type

#-------------------------Objective Function---------------------------

maximize Tax:  (sum{l in LOT_TYPE} profit[l]*COUNT[l]);

#--------------------------Constraints---------------------------------

subject to lots_avail: DEMO <= 350;															#Only 350 lots available to demolish
subject to demo_acres: .25*DEMO >= sum{l in LOT_TYPE} COUNT[l]*acres[l];					#Can only build on available land
subject to costs: DEMO*3000 + sum{l in LOT_TYPE} cost[l]*COUNT[l] <= budget;				#Can only use grant money
subject to divers {l in LOT_TYPE}: COUNT[l] >= min_percent[l]*(sum{t in LOT_TYPE} COUNT[t]);#Must meet min requirements for each lot type 


#----------------------------Data---------------------------------------

data "C:\Users\Dylan\Documents\OU\DSA5113\FINAL\dsteimel_final_p1.dat";


solve;

display DEMO;
display COUNT;
display Tax;