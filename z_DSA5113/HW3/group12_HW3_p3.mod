reset;
option solver cplex;
option cplex_options 'sensitivity';

#---------------------------Sets-------------------------------------
set SUPPLIERS;				#Possible suppliers

#------------------------Parameters----------------------------------

param cap {SUPPLIERS} >= 0;				#Max widgets per supplier
param demand_amt = 55000;


#-------------------------Decision Variables---------------------------

var WIDGETS {SUPPLIERS} >= 0;	#Widget total from each supplier
var BOOLS {SUPPLIERS} binary;	#If widget ordered from supplier
var d1 >= 0 <= 3000;			#WOW widgets up to 3k
var d2 >= 0 <= 6000;			#WOW widgets up to 6k
var d3 >= 0;					#WOW widgets over 6k
var y1 binary;					#is d1 = 3k
var y2 binary;					#is d2 = 3k

#-------------------------Objective Function---------------------------

minimize Cost: 	WIDGETS['WII']*4.95 + 
				BOOLS['WRS']*20000 + WIDGETS['WRS']*2.3 +
				BOOLS['WRS']*WIDGETS['WE']*3.95 - (BOOLS['WRS'] - 1)*WIDGETS['WE']*4.1 +
				WIDGETS['WU']*4.25 + 
				9.5*d1 + 4.9*d2 + 2.75*d3;

#--------------------------Constraints---------------------------------

subject to demand: sum{s in SUPPLIERS} WIDGETS[s] >= demand_amt;				#need enough widgets
subject to supply {s in SUPPLIERS}: WIDGETS[s] <= cap[s];						#Supplier caps
subject to bools1 {s in SUPPLIERS}: WIDGETS[s] >= BOOLS[s];						#if widgets ordered, bool on 
subject to bools0 {s in SUPPLIERS}: WIDGETS[s] <= BOOLS[s]*demand_amt;			#if bool off, no widgets ordered
subject to WE_restraints: BOOLS['WE'] + BOOLS['WII'] <= BOOLS['WRS'] + 1;		#Can't buy from WE and WII unless ordering from WRS
subject to WU_minimum: WIDGETS['WU'] >= 15000*BOOLS['WU'];						#WU has 15k order minimum
subject to WOW_linear_cost: WIDGETS['WOW'] = d1 + d2 + d3;						#WOW is sum of d1,d2,d3
subject to y1_bool: d1 >= y1*3000; 												#If y1 on, d1 = 3k
subject to y2_bool: d2 >= y2*6000;												#If y2 on, d2 = 6k
subject to logic: 6000*y2 <= d2;												#if d2 < 3000 y2 off
subject to logic1: d2 <= 6000*y1;												#If d2 > 0, y1 on
subject to logic2: d3 <= demand_amt*y2;											#If d3 > 0, y2 on

#----------------------------Data---------------------------------------

data "C:\Users\Dylan\Documents\OU\DSA5113\HW3\group12_HW3_p3.dat";


solve;

display Cost;
display WIDGETS;
display BOOLS;
