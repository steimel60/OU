reset;
option solver cplex;
option cplex_options 'sensitivity';

#---------------------------Sets-------------------------------------
set INGREDIENT;			#Ingredients in products
set PRODUCT;			#Products Created

#------------------------Parameters----------------------------------

param recipe {PRODUCT, INGREDIENT} >= 0;		#Ingredients to make 1 product
param demand {PRODUCT} >= 0;					#Minimum make requirement
param profit {PRODUCT} >= 0;					#Profit for product
param supply {INGREDIENT} >= 0;					#Available ingredients

#-------------------------Decision Variables---------------------------

var MIX {INGREDIENT, PRODUCT} >= 0;		#Ingredients used in each product
var MAKE {PRODUCT} integer >= 0;		#How much of each product is made

#-------------------------Objective Function---------------------------

maximize Profit: sum{p in PRODUCT}MAKE[p]*profit[p];

#--------------------------Constraints---------------------------------

subject to ratio: MAKE['SEMI']*5 <= MAKE['HIGH']*2;									#Ratio requirement from marketings
subject to demands {p in PRODUCT}: MAKE[p] >= demand[p];							#Meet minimum demand
subject to supplies {i in INGREDIENT}: sum{p in PRODUCT}MIX[i,p] <= supply[i];		#Limited to available ingredients
subject to mix {i in  INGREDIENT, p in PRODUCT}: recipe[p,i]*MAKE[p] = MIX[i,p];	#Use given recipe

#----------------------------Data---------------------------------------

data "C:\Users\Dylan\Documents\OU\DSA5113\EXAM1\problem1.dat";

solve;

display Profit;
display MAKE;
display MIX;