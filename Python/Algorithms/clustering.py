import math
from Edge import Edge
from time import clock
from UF import UF

f = open('clustering1.txt')

n = int(f.readline())

adj = [[] for i in range(n+1)]
uf = UF(n+1)
edge_lst = []

for line in f:
    u, v, cost = [int(val) for val in line.split()]
    e = Edge(u, v, cost)
    edge_lst.append(e)

start = clock()
edge_lst.sort(key=lambda e: e.weight)
# for e in edge_lst:
# print(e)


MST_edges = []
total_cost = 0
num_clusters = 4

i = 0
while uf.count > 1 + num_clusters:
    # print("Edge: " + str(i))
    e = edge_lst[i]
    u, v = e.verts()
    if not uf.connected(u, v):
        uf.union(u, v)
        # print(uf.count, len(MST_edges))

        MST_edges.append(e)
        total_cost += e.weight
    i += 1

while True:
    e = edge_lst[i]
    u, v = e.verts()
    if not uf.connected(u, v):
        space = e.weight
        break
    else:
        i += 1

end = clock()
# print(total_cost)
print(space)
print("Time: %.2fs" % (end - start))
# for e in MST_edges:
#     print(e)
