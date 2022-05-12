reset;
option solver cplex;
option cplex_options 'sensitivity';

#---------------------------Sets-------------------------------------
set PRODUCT;				#Products in question
set SILO;					#Available Silos

#------------------------Parameters----------------------------------

param cost {PRODUCT, SILO} >= 0;	#Silo-Loading cost per ton
param supply {PRODUCT} >= 0;		#Tons of each product to store
param cap {SILO} >= 0;				#Max tons per Silo
param weight_cost = .99				#Weight of how important cost is
param weight_waste = .01;			#Weight of how important empty space is

#-------------------------Decision Variables---------------------------

var STORE {PRODUCT, SILO} >= 0;		#Tons of product in silo
var BOOLS {PRODUCT, SILO} binary;	#If product is in silo
var WASTE {SILO} >= 0;		#Empty space in used silos

#-------------------------Objective Function---------------------------

minimize Cost: sum{p in PRODUCT, s in SILO}(cost[p,s]*STORE[p,s]*weight_cost+WASTE[s]*weight_waste*BOOLS[p,s]);

#--------------------------Constraints---------------------------------

subject to no_mixing {s in SILO}: sum {p in PRODUCT} BOOLS[p,s] <= 1;			#Only 1 product per silo
subject to capacity {s in SILO}: sum{p in PRODUCT} STORE[p,s] <= cap[s];		#Limited to silo capacity
subject to store_all {p in PRODUCT}: sum {s in SILO} STORE[p,s] = supply[p];	#Everything must be stored
subject to bools1 {p in PRODUCT, s in SILO}: STORE[p,s] >= BOOLS[p,s]*.001;		#If bool is on, something must be stored
subject to bools0 {p in PRODUCT, s in SILO}: STORE[p,s] <= BOOLS[p,s]*500;		#If bool is off, nothing stored
subject to emptiness {s in SILO}: WASTE[s] = cap[s] - sum{p in PRODUCT}STORE[p,s]; 

#----------------------------Data---------------------------------------

data "C:\Users\Dylan\Documents\OU\DSA5113\HW3\group12_HW3_p2.dat";

solve;

display STORE;
display BOOLS;