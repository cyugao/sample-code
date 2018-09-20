from UF import UF

# def hamming_dist(s1, s2):
#     count = 0
#     n = len(s1)
#     if n != len(s2):
#         raise ValueError
#     for i in range(n):
#         if s1[i] == s2[i]:
#             count += 1
#     return count

# print(hamming_dist('0101', '1100'))

f = open('clustering_big.txt')

s = f.readline().split()
n = int(s[0])
nbits = int(s[1])

uf = UF(n)
d = {} # hash table

# initialize
for i in range(n):
    line = f.readline()
    s = ''.join(line.split())
    if s in d:
        uf.union(d[s], i) # merge same verts
    else:
        d[s] = i

# merge pair of points with distance 1
for s, j in d.items():
    for k in range(nbits):
        # flip kth bits
        c = '1' if s[k] == '0' else '0'
        t = s[:k] + c + s[k+1:]
        if t in d:
            v = d[t]
            if not uf.connected(v, j):
                uf.union(v, j)

# merge pair of points with distance 2
for s, j in d.items():
    # iterate through all possible strings
    for k in range(nbits):
        for l in range(k+1, nbits):
        # flip kth bits
            c1 = '1' if s[k] == '0' else '0'
            c2 = '1' if s[l] == '0' else '0'
            t = s[:k] + c1 + s[k+1:l] + c2 + s[l+1:]
            if t in d:
                v = d[t]
                if not uf.connected(v, j):
                    uf.union(v, j)

# for line i

print(uf.count)
