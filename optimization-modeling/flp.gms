option optcr = 0.0;
set dept "major locations in campus" /Human, Pharmacy, Veterinary, Business, Biomedical, Cartography, Chemistry, Civil, Computer, Curriculum, Economics, Psychology, English, Environment, History, Material, Mathematics, Music, Nursing, Physics, Statistics, Animal/;
set lib  "libraries" /Art, College, Ebing, Learning, Memorial, MERIT, Robinson, Social, Steenbock/;
set loc  "dimension"  /x,y/;

scalar unitcost;
unitcost = 0.002;

parameter
    cost_lib(lib)  "opening cost of each lib"
    capacity(lib)
    dist(lib, dept)
;
option seed = 101;

parameter demand(dept)
/
Human 93
Pharmacy 88
Veterinary 51
Business 220
Biomedical 105
Cartography 118
Chemistry 360
Civil 127
Computer 383
Curriculum 277
Economics 262
Psychology 152
English 124
Environment 108
History 118
Material 110
Mathematics 166
Music 108
Nursing 100
Physics 190
Statistics 196
Animal 146
/;

table deptloc(dept,loc) "coordinates of department buildings"
$ondelim
$include school_loc.csv
$offdelim
;

table libloc(lib,loc) "coordinates of libraries"
$ondelim
$include lib_loc.csv
$offdelim
;

cost_lib(lib) = 100;
capacity(lib) = 1000;
   
dist(lib, dept) = sum(loc, abs(libloc(lib,loc) - deptloc(dept,loc)));

binary variables
    cover(lib,dept)
    open(lib);

Variable
   cost
   obj;

Equation
   total_cost
   objective
   coverConstraint
   demandConstraint
   rela
;

objective..
    obj =E= unitcost * sum((lib, dept), dist(lib, dept)* cover(lib, dept)) + cost;

demandConstraint(lib)..
    sum(dept, demand(dept) * cover(lib, dept)) =l= capacity(lib);

coverConstraint(dept)..
    sum(lib, cover(lib, dept)) =e= 1;

total_cost..
    cost =e= sum(lib, cost_lib(lib) * open(lib));
    
rela(lib)..
*    open(lib) =e= 0 + 1$(sum( dept, cover(lib, dept) ) > 0);
    sum(dept, cover(lib, dept) ) =l= card(dept)*open(lib);

Model facility /all/;
solve facility using mip minimizing obj;

scalar count;
count = sum(lib, open.l(lib));