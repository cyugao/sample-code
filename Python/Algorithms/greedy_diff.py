from sys import stdin
import numpy as np

n = int(stdin.readline())

a = [tuple(int(val) for val in line.split()) for line in stdin]

key1 = lambda x: (x[0] - x[1], x[0])
key2 = lambda x: x[0] / x[1]

a.sort(key=key2, reverse=True)
# print(a)
ws = np.array(list(map(lambda x: x[0], a)))
lCumsum = np.cumsum(list(map(lambda x: x[1], a)))
print(np.dot(ws, lCumsum))