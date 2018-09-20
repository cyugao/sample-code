from heapq import _siftdown, heappop, heappush
from sys import stdin

class Graph(object):
    """Simple graph representation"""
    def __init__(self, V=0):
        if V < 0:
            raise ValueError("Number og vertices must be nonnegative")
        self._V = V
        self._E = 0
        self._adj = [set() for i in range(V+1)]

    def fromInput(self, f):
        s = f.readline().split()
        V = int(s[0])
        E = int(s[1])
        self.__init__(V)
        for line in f:
            self.addEdge(tuple(int(val) for val in line.split()))

    def addEdge(self, e):
        u, v, w = e
        self.validate(u)
        self.validate(v)
        self._adj[u].add((v, w))
        self._adj[v].add((u, w))

    def V(self):
        return self._V

    def E(self):
        return self._E

    def validate(self, v):
        if v < 0 or v > self._V:
            raise ValueError("Illegal vertex")

    def adj(self, v):
        self.validate(v)
        return self._adj[v]

    def __str__(self):
        return "\n".join([str(v) + "-%d %d" % e for v, vEdges in enumerate(self._adj) for e in vEdges])

G = Graph()
f = open("test.txt") 
G.fromInput(f)
# print(G)
# print(G._adj)

pq = []

marked = [False for i in range(G.V()+1)]
distTo = [float('inf') for i in range(G.V()+1)]
vertexTo = [None for i in range(G.V()+1)]
qp = [None for i in range(G.V()+1)]

def update(v, dist):
    if vertexTo[v]:
        pq[qp[v]] = dist
        _siftdown(pq, 0, qp[v])
        return qp[v]
    else:
        heappush(pq, (dist, v))
        return len(pq) - 1

distTo[1] = 0
heappush(pq, (0, 1)) # push the first node

while pq:
    _, u = heappop(pq)
    marked[u] = True
    # print(G.adj(u))
    for e in G.adj(u):
        v, w = e
        # print(v, w, distTo[v])
        if marked[v]:
            continue
        if w < distTo[v]:
            # print(w)
            print(u, e, "---", vertexTo[v], qp[v])
            qp[v] = update(v, w)
            distTo[v] = w
            vertexTo[v] = u

total = 0
print(distTo)
print(vertexTo)
for i in range(2, G.V() + 1):
    w, v = distTo[u], vertexTo[u]
    print("%d-%d: %d" % (u, v, w))
    total = total + w

# print(total)