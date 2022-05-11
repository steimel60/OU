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
param production_cost {PROD} >=0;	#Costs excluding fruit costs
param supplies_cost = 1736000;

#Supplies
param supply {GRADE} >= 0;		#Pounds of available grapes
param rating {GRADE} >= 0;		#Numerical Value for grape grade
param fruit_cost {GRADE} >=0;	#Cost per pound of each grade

#-------------------------Decision Variables---------------------------

var Mix {PROD, GRADE} >=0;		#Pounds of each grade of raisin per product
var Make {PROD};				#Count of each product to make
var Profit_Contribution {PROD};	#Profit made per product

#-------------------------Objective Function---------------------------

maximize Profit: sum{p in PROD} Profit_Contribution[p];

#--------------------------Constraints---------------------------------

subject to recipe {p in PROD}: Make[p] <= (sum{g in GRADE}Mix[p,g])/rate[p];	#Can only make as many products as we have ingredients for
subject to supplies {g in GRADE}: sum{p in PROD} Mix[p,g] <= supply[g];			#Can only use as many ingredients as we have
subject to quality {p in PROD}: (sum{g in GRADE} rating[g]*Mix[p,g]) >= sum{g in GRADE}Mix[p,g]*min_avg[p]; #Quality meets product requirements
subject to market {p in PROD}: Make[p] <= demand[p];							#Can only sell as much as is demanded
subject to money {p in PROD}: Profit_Contribution[p] = (Make[p]*(sales_price[p]-production_cost[p]) - sum{g in GRADE} Mix[p,g]*fruit_cost[g]); #Profit per product

#----------------------------Data---------------------------------------

data "C:\Users\Dylan\Documents\OU\Classes\DSA5113\HW2\Problem_1.dat";

solve;

display Make;
display Profit_Contribution;
display Profit;
display supplies, supplies.lb, supplies.ub, supplies.up, supplies.down;

