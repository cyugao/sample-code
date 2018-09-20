import math
from Edge import Edge
from time import clock
from UF import UF

f = open('edges1.txt')

s = f.readline().split()
n = int(s[0])
num_edges = int(s[1])

adj = [[] for i in range(n+1)]
uf = UF(n+1)
edge_lst = [None] * num_edges

for i in range(num_edges):
    line = f.readline()
    u, v, cost = [int(val) for val in line.split()]
    e = Edge(u, v, cost)
    edge_lst[i] = e

start = clock()
edge_lst.sort(key=lambda e: e.weight)
# for e in edge_lst:
# print(e)


MST_edges = []
total_cost = 0

i = 0
while len(MST_edges) != n-1:
    e = edge_lst[i]
    u, v = e.verts()
    if not uf.connected(u, v):
        uf.union(u, v)
        MST_edges.append(e)
        total_cost += e.weight
        # print(uf.count)
    i += 1

end = clock()
print(total_cost)
print("Time: %.2fs" % (end - start))
for e in MST_edges:
    print(e)


