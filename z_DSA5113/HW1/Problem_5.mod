reset;

set PROD;
set STAGE;

param rate {PROD, STAGE} >= 0;			#tons produced per hour
param avail {STAGE} >= 0;				#hours of work available
param profit {PROD};					#profit per ton
param commit {PROD} >= 0;				#minimum
param market {PROD} >= 0;				#limit on tons sold in a week
param share {PROD} >= 0;				#min share of total weight 

var Make {p in PROD} >= commit[p], <= market[p];	#tons produced

maximize Total_Profit: sum {p in PROD} profit[p]*Make[p];

subject to Time {s in STAGE}: sum {p in PROD} (1/rate[p,s])*Make[p] = avail[s];

data "C:\Users\Dylan\Documents\OU\Classes\DSA5113\HW1\Problem_5.dat";

solve;

display commit, Make, market;
display Time;
display Total_Profit;