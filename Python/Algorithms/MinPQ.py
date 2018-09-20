"""
Adapt from java code in Algorithms, Robert Sedgewick
"""

class MinPQ(object):
    """
    Simple IndexMinPQ implementation

    private members:

    capacity: maximum number of elements on PQ
    n: current size of PQ
    pq: binary heap (index starts from 1)
    qp: used to look up items -- qp[pq[i]] = pq[qp[i]] = i
    keys: keys[i] -- priority of i
    """

    def __init__(self, capacity):
        """
        Initialize empty index-pq with capacity given
        """
        if capacity < 0:
            raise ValueError("Capacity must be nonnegative")
        self._capacity = capacity
        self._n = 0
        self._pq = [None] * (capacity + 1)

    def isEmpty(self):
        return self._n == 0

    def size(self):
        return self._n

    def insert(self, key):
        self._n += 1
        if self._n == self._capacity:
            self._pq.extend([None] * self._capacity)
            self._capacity *= 2
        self._pq[self._n] = key
        self._swim(self._n)

    def extract_min(self):
        if (self._n == 0):
            raise IndexError
        min_item = self._pq[1]
        self._swap(1, self._n)
        self._pq[self._n] = None
        self._n -= 1
        self._sink(1)
        return min_item

        
    def _greater(self, i, j):
        return self._pq[j] < self._pq[i]

    def _swap(self, i, j):
        temp = self._pq[i]
        self._pq[i] = self._pq[j]
        self._pq[j] = temp

    def _swim(self, k):
        self._pq[0] = self._pq[k]
        while self._greater(k // 2, k):
            self._swap(k, k // 2)
            k = k // 2

    def _sink(self, k):
        while 2*k <= self._n:
            j = 2*k
            if j < self._n and self._greater(j, j+1):
                j = j + 1
            if self._greater(k, j):
                self._swap(k, j)
                k = j
            else:
                break

if __name__ == '__main__':
    from Edge import Edge
    e1 = Edge(1, 2, 4)
    e2 = Edge(3, 2, 5)
    e3 = Edge(1, 4, 3)
    pq = MinPQ(5)
    pq.insert(e1)
    pq.insert(e2)
    pq.insert(e3)
    while not pq.isEmpty():
        e = pq.extract_min()
        print(e)

