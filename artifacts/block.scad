// SCD biprism, one physical handedness. No clearance or connectors.
side = 30; h = 2/5; lambda = 1/3;
a = [1,0,0]; b = [1/3,2*sqrt(2)/3,0];
c = lambda*b + [0,0,h]; d = lambda*a - [0,0,h];
scale(side) translate([0,0,h])
polyhedron(points=[[0,0,0],a,b,a+b,c,a+c,d,b+d],
  faces=[[6, 0, 1], [3, 2, 7], [4, 0, 2], [3, 1, 5], [6, 1, 3, 7], [2, 0, 6, 7], [4, 2, 3, 5], [5, 1, 0, 4]]);
