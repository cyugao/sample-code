import math
from Edge import Edge
from MinPQ import MinPQ
from time import clock

f = open('edges.txt')

s = f.readline().split()
n = int(s[0])
num_edges = int(s[1])

adj = [[] for i in range(n+1)]

for line in f:
    u, v, cost = [int(val) for val in line.split()]
    e = Edge(u, v, cost)
    adj[u].append(e)
    adj[v].append(e)

def timeit(func):
    def inner(*args, **kwargs):
        start = clock()
        ret = func(*args, **kwargs)
        end = clock()
        print("Finished in %.2fs" % (end - start))
        return ret
    return inner

@timeit
def prim_naive(adj):
    n = len(adj) - 1
    MST = set()
    MST.add(1)

    MST_edges = []
    total_cost = 0

    for i in range(n-1):
        min_cost = math.inf
        edge = None
        for u in MST:
            for e in adj[u]:
                v = e.other(u)
                if v in MST:
                    continue
                if e.weight < min_cost:
                    edge = e
                    min_cost = e.weight
        total_cost += min_cost
        u, v = edge.verts()
        if u in MST:
            MST.add(v)
        else:
            MST.add(u)
        MST_edges.append(edge)

    return total_cost, MST_edges

@timeit
def prim_edge_pq(adj):
    n = len(adj) - 1
    MST = set()
    MST.add(1)

    MST_edges = []
    total_cost = 0
    pq = MinPQ(n)
    for e in adj[1]:
        pq.insert(e)

    while len(MST) != n:
        edge = pq.extract_min()
        # print(edge)
        u = edge.either()
        v = edge.other(u)
        if u in MST and v in MST:
            continue
        if u in MST:
            s = v
        else:
            s = u
        MST.add(s)
        MST_edges.append(edge)
        total_cost += edge.weight
        for e in adj[s]:
            pq.insert(e)

    return total_cost, MST_edges

# start = clock()
total_cost, MST_edges = prim_naive(adj)
# end = clock()
print(total_cost)
# print("Time: %.2fs" % (end - start))
# # for e in MST_edges:
#     print(e, end=', ')

# start = clock()
total_cost, MST_edges = prim_edge_pq(adj)
# end = clock()
print(total_cost)
# print("Time: %.2fs" % (end - start))
# for e in MST_edges:
#     print(e, end=', ')


