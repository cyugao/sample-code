option optcr=0;
set
group /Art, College, Ebing, Learning, Memorial, MERIT, Robinson, Social, Steenbock/
node /Art,College,Ebing,Learning,Memorial,MERIT,Robinson,Social,Steenbock,Animal,Biomedical,Business,Cartography,Chemistry,Civil,Computer,Curriculum,Economics,English,Environment,History,Human,Material,Mathematics,Music,Nursing,Pharmacy,Physics,Psychology,Statistics,Veterinary/
trans /"bike", "car"/
loc /x,y/
;
alias(node, i, j, l);
alias(trans, t)

parameter
unit_costt(t) /bike 0, car 0.002/
avai(t) /bike 10, car 3/
cap(t) /bike 200, car 1000/
dist(node, node)
upfront_costt(t) /bike 2, car 10/
;

scalar M;
M = smax(t, cap(t));

parameter demand(node)
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

table node_loc(node, loc)
$ondelim
$include node_loc.csv
$offdelim
;

table node_type(group, node)
$ondelim
$include node_type.csv
$offdelim
;

dist(i, j) = sum(loc, abs(node_loc(i,loc) - node_loc(j,loc)));

scalar
g;
* set V only contains one library and its department buildings
* V(group, node) V has several groups, and each group has one lib and some dep buildings;
positive variables
u(i, t);

binary variables
route(node, node,t)
* out(i,t), in(j,t);
;

variables
trans_cost
vrp_obj;

equations
* out_eq
* in_eq
vrp1
vrp2
vrp3
vrp4
same_trans
mtz
total
use_trans
u_up
;


* out_eq(i,t,group)$(ord(group) = g and node_type(group, i) ne 0)..
* out(i,t) =e= sum(j$(node_type(group, j) ne 0), route(i,j,t));

* in_eq(j,t,group)$(ord(group) = g and node_type(group, j) ne 0)..
* out(j,t) =e= sum(i$(node_type(group, i) = 1), route(i,j,t));

total(group)$(ord(group) = g)..
    vrp_obj =e= sum((i, j, t)$(node_type(group, i) ne 0 and
                   node_type(group, j) ne 0), unit_costt(t) * dist(i, j) * route(i, j, t))
    + trans_cost;
    
use_trans(i,group)$(node_type(group, i) = 2 and ord(group) = g)..
    trans_cost =e= sum((t, j)$(node_type(group, j) = 1), route(i, j, t) * upfront_costt(t));
   
vrp1(j, group)$(node_type(group, j) = 1 and ord(group) = g)..
    sum((i,t)$(node_type(group, i) ne 0 and not sameas(i,j)),route(i, j, t)) =e= 1;
     
vrp2(i, group)$(node_type(group, i) = 1 and ord(group) = g)..
    sum((j,t)$(node_type(group, j) ne 0 and not sameas(i,j)),route(i, j, t)) =e= 1;

vrp3(j, t, group)$(node_type(group, j) = 2 and ord(group) = g)..
    sum(i$(node_type(group, i) = 1), route(i, j, t)) =l= avai(t);

vrp4(i, t, group)$(node_type(group, i) = 2 and ord(group) = g)..
    sum(j$(node_type(group, j) = 1), route(i, j, t)) =l= avai(t);

mtz(i, j, t, group)$(node_type(group, i) = 1 and node_type(group, j) = 1 and not sameas(i,j) and ord(group) = g)..
u(j, t) =g= u(i, t) + demand(j) * route(i, j,t) - cap(t) * (1 - route(i, j, t));

same_trans(i, t, group)$(node_type(group, i) = 1 and ord(group) = g)..
sum(j$(node_type(group, j) ne 0 ), route(i, j, t)) =e= sum(l$(node_type(group, l) ne 0),route(l,i,t));

u_up(i, t, group)$(node_type(group, i) = 1 and ord(group) = g)..
u(i,t) =l= (1 - sum(j$(node_type(group, j) ne 0), route(i, j, t))) * (M-cap(t)) + cap(t);

u.lo(i, t) = demand(i);

Model vrp /all/;
* g = 9;
* solve vrp using mip minimizing vrp_obj;
scalar total_cost;
total_cost = 0;

for(g = 1 to card(group),

u.l(i, t) = 0;
route.l(node, node,t) = 0;
trans_cost.l = 0;
vrp_obj.l = 0;
solve vrp using mip minimizing vrp_obj;
total_cost = total_cost + vrp_obj.l;
);

display total_cost;
