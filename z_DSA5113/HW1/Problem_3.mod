reset;

var a >= 0;                   
var b >=0;
var c >=0;
var d >=0;
var e >=0;
var loan <= 1;

maximize earnings: .043*a + .027*b + .025*c + .022*d +.045*e - .0275*loan;
subject to total: a+b+c+d+e <= 10 + loan;
subject to GovAgency: b+c+d >= 4;
subject to quality: .6*a + .6*b - .4*c -.4*d +3.6*e <= 0;
subject to maturity: 4*a + 10*b -c -2*d - 3*e <= 0;

solve;

display a;
display b;
display c;
display d;
display e;
display loan;
display earnings;



