reset;
option solver cplex;
option cplex_options 'sensitivity';

#---------------------------Sets-------------------------------------
set PROD;					#Product created
set GRADE;					#Grade of grapes

#------------------------Parameters----------------------------------

#Products
param min_avg {PROD} >= 0;			#Min average grade of ingredients
param demand {PROD} >= 0;			#Demand for product
param rate {PROD} >= 0;				#Pounds of grapes needed for product
param sales_price {PROD} >= 0;		#Sale price of the product
param other_cost {PROD} >=0;	#Costs excluding fruit costs
param bollman_fruit_cost {PROD} >=0;	#Costs excluding fruit costs
param thomas_fruit_cost {PROD} >=0;	#Costs excluding fruit costs

#Supplies
param supply {GRADE} >= 0;		#Pounds of available grapes
param rating {GRADE} >= 0;		#Numerical Value for grape grade
param fruit_cost {GRADE} >=0;	#Cost per pound of each grade

#-------------------------Decision Variables---------------------------

var Mix {PROD, GRADE} >=0;	#Pounds of each grade of raisin per product
var Make {PROD};			#Count of each product to make
var Qlty {PROD};			#Avg quality of final products

#-------------------------Objective Function---------------------------

maximize Profit: sum{p in PROD}(Make[p]*(sales_price[p]-other_cost[p]-thomas_fruit_cost[p]));

#--------------------------Constraints---------------------------------

subject to recipe {p in PROD}: Make[p] <= (sum{g in GRADE}Mix[p,g])/rate[p];	#Can only make as many products as we have ingredients for
subject to supplies {g in GRADE}: sum{p in PROD} Mix[p,g] <= supply[g];			#Can only use as many ingredients as we have
subject to quality {p in PROD}: (sum{g in GRADE} rating[g]*Mix[p,g]) >= sum{g in GRADE}Mix[p,g]*min_avg[p]; #Quality meets product requirements
subject to market {p in PROD}: Make[p] <= demand[p];							#Can only sell as much as is demanded

#----------------------------Data---------------------------------------

data "C:\Users\Dylan\Documents\OU\Classes\DSA5113\HW2\problem_1d.dat";

solve;

display Make;
display Mix;
display Profit;
display thomas_fruit_cost;
display supplies, supplies.lb, supplies.ub, supplies.up, supplies.down;

