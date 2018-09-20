
class MaxPQ(object):
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

    def extract_max(self):
        if (self._n == 0):
            raise IndexError
        max_item = self._pq[1]
        self._swap(1, self._n)
        self._pq[self._n] = None
        self._n -= 1
        self._sink(1)
        return max_item

        
    def _less(self, i, j):
        return self._pq[i][0] < self._pq[j][0]

    def _swap(self, i, j):
        temp = self._pq[i]
        self._pq[i] = self._pq[j]
        self._pq[j] = temp

    def _swim(self, k):
        self._pq[0] = self._pq[k]
        while self._less(k // 2, k):
            self._swap(k, k // 2)
            k = k // 2

    def _sink(self, k):
        while 2*k <= self._n:
            j = 2*k
            if j < self._n and self._less(j, j+1):
                j = j + 1
            if self._less(k, j):
                self._swap(k, j)
                k = j
            else:
                break

if __name__ == '__main__':
    e1 = (4, 1, 2)
    e2 = (5, 3, 2)
    e3 = (3, 1, 4)
    pq = MaxPQ(5)
    pq.insert(e1)
    pq.insert(e2)
    pq.insert(e3)
    while not pq.isEmpty():
        e = pq.extract_max()
        print(e)

