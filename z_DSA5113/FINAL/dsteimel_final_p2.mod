reset;
option solver cplex;
option cplex_options 'sensitivity';

var x1 binary;
var x2 binary;
var x3 binary;
var x4 >= 0;

minimize ans: x4;

subject to cons: 2*x1 + 2*x2 + 2*x3 + x4 = 5;
subject to cons1: x1=1;
subject to cons2: x2=1;
#subject to cons3: x3=0;


solve;

display x1;
display x2;
display x3;
display x4;