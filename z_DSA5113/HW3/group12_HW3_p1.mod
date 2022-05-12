reset;
option solver cplex;
option cplex_options 'sensitivity';

#---------------------------Sets-------------------------------------
set GENERATOR;				#Generators in question
set PERIOD;					#Period of production

#------------------------Parameters----------------------------------

param S {GENERATOR} >= 0;		#Start-up cost
param F {GENERATOR} >= 0;		#Fixed cost of running per period
param C {GENERATOR} >= 0;		#Cost per megawatt
param U {GENERATOR} >= 0;		#Production limit per period
param min_prod {PERIOD} >=0;	#Minimum production per period

#-------------------------Decision Variables---------------------------

var V {GENERATOR, PERIOD} >= 0;		#Megawatts generated
var G {GENERATOR, PERIOD} binary;	#Startup bools

#-------------------------Objective Function---------------------------

minimize Cost: sum {g in GENERATOR} (G[g,'P1']*(S[g]+F[g]+C[g]*V[g,'P1'])+G[g,'P2']*(S[g]-S[g]*G[g,'P1']+F[g]+C[g]*V[g,'P2']));

#--------------------------Constraints---------------------------------

subject to demand {p in PERIOD}: sum {g in GENERATOR} V[g,p] >= min_prod[p];	#Have to meet production requirements
subject to supply {g in GENERATOR, p in PERIOD}: V[g,p] <= U[g];				#Each generator has production limits
subject to bools {p in PERIOD, g in GENERATOR}: V[g,p] <= G[g,p]*5000;			#Generator bool must be on to produce
#----------------------------Data---------------------------------------

data "C:\Users\Dylan\Documents\OU\Classes\DSA5113\HW3\group12_HW3_p1.dat";

solve;

display V;
display G;
display Cost;