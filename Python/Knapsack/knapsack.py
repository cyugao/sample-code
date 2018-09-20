import sys
from time import clock
from collections import deque

def timeit(func):
    def inner(*args, **kwargs):
        start = clock()
        ret = func(*args, **kwargs)
        end = clock()
        print("Finished in %.2fs" % (end - start))
        return ret
    return inner

def f(w, v, max_cap):
    item_count = len(w)
    dp = [[0] * (max_cap+1) for i in range(item_count)]
    for i in range(1, item_count):
        for cap in range(1, max_cap+1):
            if w[i] > cap:
                dp[i][cap] = dp[i-1][cap]
            else:
                dp[i][cap] = max(dp[i-1][cap], dp[i-1][cap - w[i]] + v[i])
    return dp

def print_optimal_recursive(dp, w, n, cap):
    # print(n, cap)
    if dp[n][cap] == 0:
        return ""
    else:
        if dp[n][cap] == dp[n-1][cap]:
            return print_optimal_recursive(dp, w, n-1, cap)
        else:
            return print_optimal_recursive(dp, w, n-1, cap - w[n]) + "-" + str(n)

def print_optimal(dp, w, n, cap):
    # result = []
    result = set()
    while dp[n][cap] != 0:
        if dp[n][cap] != dp[n-1][cap]:
            # result.append(str(n))
            result.add(n)
            cap -= w[n]
        n -= 1
    # return '-'.join(reversed(result))
    return result


# dp = f(w, v, cap)
# print(print_optimal(dp, w, n, cap))

def mem(w, v, cap, j, memo={}):
    if j == 0:
        return 0
    if (j, cap) in memo:
        return memo[(j, cap)]
    if w[j] <= cap:
        ans = max(mem(w, v, cap, j-1),
                   v[j] + mem(w, v, cap - w[j], j-1))
    else:
        ans = mem(w, v, cap, j-1)
    memo[(j, cap)] = ans
    # if j == len(w) - 1:
    #     print(memo)
    return ans

def greedy(w, v, cap):
    n = len(w)
    rank = sorted(range(n), key=lambda i: v[i] / w[i], reverse=True)
    cur_cap = 0
    cur_val = 0
    for j in rank:
        if cur_cap + w[j] <= cap:
            cur_cap += w[j]
            cur_val += v[j]
    return cur_val

def bound(v, w, i, cap_remain):
    n = len(v)
    rank = sorted(range(i, n), key=lambda i: v[i] / w[i], reverse=True)
    cur_cap = 0
    cur_val = 0

    p = n - i
    j = 0
    while j < p:
        idx = rank[j]
        if cur_cap + w[idx] <= cap_remain:
            cur_cap += w[idx]
            cur_val += v[idx]
            j += 1
        else:
            break
    if j < p:
        # print(cur_cap)
        cur_val += v[idx] / w[idx] * (cap_remain - cur_cap)
    return cur_val

def solve(file, memo=False):
    fp = open(file)
    firstline = fp.readline().split()
    cap = int(firstline[1])
    n = int(firstline[0])
    vs = [None] * (n+1)
    ws = [None] * (n+1)
    vs[0] = 0
    ws[0] = 0
    for i in range(1, n+1):
        line = fp.readline()
        vw = line.split()
        vs[i] = int(vw[0])
        ws[i] = int(vw[1])
    # print(vs[:10])
    if memo:
        return mem(ws, vs, cap, n)
    else:
        dp = f(ws, vs, cap)
        # print("???")
        print(print_optimal(dp, ws, n, cap))
        return dp[n][cap]


def depth_first(w, v, cap, i, best):
    if i == len(w):
        return


if __name__ == '__main__':
    # sys.setrecursionlimit(15000)
    print(solve("ks_200_0", True))
    # print(solve("knapsack_small.txt", True))
    # print(mem(w, v, cap, n))
    # print(f(w, v, cap))

    # vs = [4, 9, 10]
    # ws = [2, 3, 4]
    # cap = 6
    # print(greedy(ws, vs, cap))
    # print(bound(vs, ws, 0, 8))