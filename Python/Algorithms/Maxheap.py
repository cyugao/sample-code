
class Maxheap(object):
    """
    Simple IndexMinPQ implementation

    private members:

    capacity: maximum number of elements on PQ
    n: current size of PQ
    pq: binary heap (index starts from 1)
    qp: used to look up items -- qp[pq[i]] = pq[qp[i]] = i
    keys: keys[i] -- priority of i
    """

    def __init__(self, a):
        """
        Initialize empty index-pq with capacity given
        """
        n = len(a)
        self._n = n
        self._pq = [0] + list(a)
        
    def sort(self):
        # print(self._pq)
        for i in range(self._n // 2, 0, -1):
            # print("Sink: " + str(self._pq[i]))
            self._sink(i)
        # print(self._pq)
        for j in range(1, self._n):
            self._swap(1, self._n)
            self._n -= 1
            self._sink(1)
        return self._pq


    def isEmpty(self):
        return self._n == 0

    def size(self):
        return self._n

    # def insert(self, key):
    #     self._n += 1
    #     if self._n == self._capacity:
    #         self._pq.extend([None] * self._capacity)
    #         self._capacity *= 2
    #     self._pq[self._n] = key
    #     self._swim(self._n)

    def extract_min(self):
        if (self._n == 0):
            raise IndexError
        min_item = self._pq[1]
        self._swap(1, self._n)
        self._pq[self._n] = None
        self._n -= 1
        self._sink(1)
        return min_item

        
    def _less(self, i, j):
        return self._pq[i] < self._pq[j]

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
                # print(self._pq[k], self._pq[j])
                self._swap(k, j)
                k = j
            else:
                break


