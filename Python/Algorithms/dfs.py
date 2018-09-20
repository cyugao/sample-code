n = 6
a = [None] * 6
marked = [False] * 6
# count = 0

def dfs(t, a):
    # global count
    if t == n:
        print(a)
        return
        # count += 1
    for i in range(n):
        if not marked[i]:
            a[t] = i
            marked[i] = True
            dfs(t+1, a)
            marked[i] = False

# dfs(0, a)
# print(count)

a = list(range(6))
def swap(a, i, j):
    t = a[i]
    a[i] = a[j]
    a[j] = t


def dfs_v2(t, a):
    if t == n:
        print(a)
        return
    for i in range(t, n):
        swap(a, i, t)
        dfs_v2(t+1, a)
        swap(a, i, t)

dfs_v2(0, a)

