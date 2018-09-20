"""
Adapt from java code in Algorithms, Robert Sedgewick
"""

class IndexMinPQ(object):
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
        self._dict = {}
        self._keys = [None] * (capacity + 1)

    def isEmpty(self):
        return self._n == 0

    def contains(self, i):
        if i < 0 or i >= self._capacity:
            raise ValueError
        return self._qp[i] != None

    def size(self):
        return self._n

    def insert(self, i, key):
        if i < 0 or i >= self._capacity:
            raise ValueError
        if self.contains(i):
            raise ValueError("Index already in PQ")
        self._n += 1
        self._qp[i] = self._n
        self._pq[self._n] = i
        self._keys[i] = key
        self._swim(i)

    def extract_min(self):
        if (self._n == 0):
            raise KeyError
        min_idx = self._pq[1]
        min_item = self._qp[min_idx], self._keys[min_idx]
        self._swap(1, self._n)
        self._pq[self._n] = None
        self._n -= 1
        self._sink(1)
        self._keys[min_idx] = None
        self._qp[min_idx] = None
        return min_item

    def changeKey(self, i, key):
        if i < 0 or i >= self._capacity:
            raise ValueError
        if not self.contains(i):
            raise KeyError("Index not in PQ")
        self._keys[i] = key
        self._swim(self._qp[i])
        self._sink(self._qp[i])
        
    def _greater(self, i, j):
        return self._keys[j] < self._keys[i]

    def _swap(self, i, j):
        temp = self._pq[i]
        self._pq[i] = self._pq[j]
        self._pq[j] = temp
        self._qp[self._pq[i]] = i
        self._qp[self._pq[j]] = j

    def _swim(self, k):
        self._keys[0] = self._keys[k]
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



        