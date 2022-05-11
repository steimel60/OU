reset;
option solver cplex;
option cplex_options 'sensitivity';

#------------------------Parameters----------------------------------

param resources = 1000;		#Available plastic
param labor = 40*60;		#Available Labor
param cap = 700;			#Production cap
param M = 10000;			#Big M

#-------------------------Decision Variables---------------------------

var RAY >= 0;
var ZAP >= 0;
var z binary;

#-------------------------Objective Function---------------------------

maximize Profit: 8*RAY+5*ZAP;

#--------------------------Constraints---------------------------------

#Previous
subject to supplies: RAY*2+ZAP <= resources;			#Limited to available ingredients
subject to workforce: 3*RAY+4*ZAP <= labor;				#Limited to available labor
subject to production_cap: RAY+ZAP <= cap;				#Given max units
subject to difference: RAY-ZAP<=350;					#Given max difference
#Exam Constraint
subject to bool: RAY+ZAP-400 <= z*M;					#if over 400 units z = 1
subject to quiz_const: RAY+ZAP <= 400+M*z;				#if z=0, under 400 units cap
subject to quiz_const2: (ZAP+RAY)*.7 <= ZAP+M*(1-z);	#if z=1, constrain to ratio

solve;

display Profit;
display RAY;
display ZAP;
display z;
