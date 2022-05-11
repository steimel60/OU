reset;
option solver cplex;  

set MEDIA;

var tv >= 0;
var mag >= 0;
var radio >= 0;

maximize obj: 1.8*tv + mag + .25*radio;

subject to budget: .02*tv + .01*mag + .002*radio<= 1;
subject to tvTime: tv >= 10;
subject to manPower: 3*mag + tv + .1429*radio <= 100; #Part B
subject to magMin: mag >= 2;
subject to radioCap: radio <= 120;

solve;

display obj;
display tv;
display mag;
display radio;

