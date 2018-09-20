class UF(object):
    """docstring for UF"""
    def __init__(self, n):
        if n < 0:
            raise ValueError
        self.count = n
        self.parent = [i for i in range(n)]
        self.rank = [0] * n

    def find(self, p):
        while p != self.parent[p]:
            self.parent[p] = self.parent[self.parent[p]]
            p = self.parent[p]
        return p

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)
        if self.rank[rootP] < self.rank[rootQ]:
            self.parent[rootP] = rootQ
        elif self.rank[rootP] > self.rank[rootQ]:
            self.parent[rootQ] = rootP
        else:
            self.parent[rootQ] = rootP
            self.rank[rootP] += 1
        self.count -= 1

if __name__ == '__main__':
    uf = UF(6)
    uf.union(1,2)
    uf.union(1,3)
    uf.union(0,4)
    print(uf.connected(2,3))


        