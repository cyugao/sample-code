def cut_rod(p, n):
    result = [None for _ in range(n+1)]
    result[0] = 0
    for i in range(1, n+1):
        result[i] = max([result[i-j] + p[j] for j in range(1, i+1)])
    return result

p = [0, 1, 5, 8, 9, 10, 17, 17, 20, 24, 30]

# print(cut_rod(p, 10))

# Algorithmic design

# Ex.1 find ind. set in a path G with largest total weight

def max_weight(w):
    n = len(w)
    if (n == 1): return w
    result = [None for _ in range(n)]
    result[0] = w[0]
    result[1] = max(w[0], w[1])
    for i in range(2, n):
        result[i] = max(result[i-1], result[i-2] + w[i])
    return result

def max_weight_with_choice(w):
    n = len(w)
    if (n == 1): return w
    choice = [False for _ in range(n)]
    result = [None for _ in range(n)]
    result[0] = w[0]
    choice[0] = True
    if w[0] < w[1]:
        choice[1] = True
        result[1] = w[1]
    else:
        result[1] = w[0]
    for i in range(2, n):
        temp = result[i-2] + w[i]
        if temp > result[i-1]:
            choice[i] = True
            result[i] = temp
        else:
            result[i] = result[i-1]
    return result, choice

def max_weight_print_choice(choice):
    n = len(choice)
    j = n-1
    sol = []
    while j >= 0:
        if choice[j]:
            sol.append(j)
            j -= 2
        else:
            j -= 1
    return list(reversed(sol))

def test_max_weight():
    print(max_weight([1,8,6,3,6])) # 8+6=14
    print(max_weight([3,5,4]))     # 3+4=7
    print(max_weight([9,4,4,9]))   # 9+9=18

    print("Test case #1:")
    result, choice = max_weight_with_choice([1,8,6,3,6])
    print(result[-1], ":", max_weight_print_choice(choice))

    print("Test case #2:")
    result, choice = max_weight_with_choice([3,5,4])
    print(result[-1], ":", max_weight_print_choice(choice))

    print("Test case #3:")
    result, choice = max_weight_with_choice([9,4,4,9])
    print(result[-1], ":", max_weight_print_choice(choice))

# test_max_weight()

# Ex. 8
x = [1, 10, 10, 1]
f = [1, 2, 4, 8]

def robot_attack(xs, fs):
    n = len(xs)
    opt = [0] * (n+1)
    choice = [None] * n
    for j in range(n-1, -1, -1):
        mmax = 0
        choice_j = None

        for k in range(j, n):
            s = opt[k+1] + min(x[k], f[k-j])
            if s > mmax:
                mmax = s
                choice_j = k
        opt[j] = mmax
        choice[j] = choice_j
    return opt, choice

def robot_attack_print_choice(choice):
    n = len(choice)
    choice_set = set()
    i = 0
    while i != n:
        i = choice[i]
        choice_set.add(i)
        i = i + 1
    return choice_set

# opt, choice = robot_attack(x, f)
# print(robot_attack_print_choice(choice))


# Ex. 10
def machine(a, b):
    n = len(a)
    if len(b) != n:
        raise ValueError
    dpa = [None] * n
    dpb = [None] * n
    dpa[0] = a[0]
    dpb[0] = b[0]
    for i in range(1, n):
        dpa[i] = max(dpa[i-1] + a[i], dpb[i-1])
        dpb[i] = max(dpb[i-1] + b[i], dpa[i-1])
    # print(dpa, dpb)
    return max(dpa[-1] ,dpb[-1])

# a = [10, 1, 1, 10]
# b = [5, 1, 20, 20]
# print(machine(a, b))

# Ex. 11
def two_companies(r, c, seq):
    n = len(seq)
    dp = [None] * (n+1)
    dp[-1] = 0
    for i in range(1, 4):
        dp[n-i] = dp[n-i+1] + seq[n-i] * r
    for i in range(n-4, -1, -1):
        dp[i] = min(dp[i+1] + seq[i] * r,
                    dp[i+4] + 4*c)
    return dp[0]

r = 1
c = 10
v = [11,9,9,12,12,12,12,9,9,11]
print(two_companies(r, c, v))



