from time import clock
from random import random
from random import shuffle
import matplotlib.pyplot as plt
from Maxheap import Maxheap


CUTOFF = 8

def timeit(func):
    def inner(*args, **kwargs):
        start = clock()
        ret = func(*args, **kwargs)
        end = clock()
        return ret, end - start
    return inner

def is_sorted(a):
    return all(a[i] <= a[i+1] for i in range(len(a)-1))

def swap(a, i, j):
    t = a[i]
    a[i] = a[j]
    a[j] = t

@timeit
def quick_sort(a, randomized=True):
    if randomized:
        shuffle(a)
    quick(a, 0, len(a)-1)

def quick(a, lo, hi):
    if (lo >= hi):
        return
    v = a[lo]
    i = lo
    j = hi + 1
    while True:
        i += 1
        while a[i] < v:
            if i == hi:
                break
            i += 1
        j -= 1
        while a[j] > v:
            j -= 1
        if i >= j:
            break
        swap(a, i, j)
    # print("pivot" + str(lo) + "---", a)
    swap(a, lo, j)
    quick(a, lo, i-1)
    quick(a, i+1, hi)

@timeit
def quick_sort_cutoff(a, randomized=True):
    if randomized:
        shuffle(a)
    quick_cutoff(a, 0, len(a)-1)
    # insertion_sort(a)

def quick_cutoff(a, lo, hi):
    if lo >= hi:
        return
    if hi - lo <= CUTOFF:
        insertion(a, lo, hi)
        return
    v = a[lo]
    i = lo
    j = hi + 1
    while True:
        i += 1
        while a[i] < v:
            if (i == hi):
                break
            i += 1
        j -= 1
        while a[j] > v:
            j -= 1
        if i >= j:
            break
        swap(a, i, j)
    # print("pivot" + str(lo) + "---", a)
    swap(a, lo, j)
    quick(a, lo, i-1)
    quick(a, i+1, hi)

def insertion(a, lo, hi):
    for i in range(lo+1, hi+1):
        t = a[i]
        j = i - 1
        while j >= lo and a[j] > t:
            j -= 1
        for k in range(i, j+1, -1):
            a[k] = a[k-1]
        a[j+1] = t


@timeit
def insertion_sort(a):
    n = len(a)
    for i in range(1, n):
        t = a[i]
        j = i - 1
        while j >= 0 and a[j] > t:
            j -= 1
        for k in range(i, j+1, -1):
            a[k] = a[k-1]
        a[j+1] = t
        # print(a)

@timeit
def merge_sort(a):
    return msort(a)

def msort(a):
    n = len(a)
    if n < 2:
        return a
    mid = (n-1) // 2
    left = msort(a[:mid+1])
    right = msort(a[mid+1:])
    return merge(left, right)

def merge(left, right):
    # assume left and right already sorted
    i = j = 0
    result = []
    m = len(left)
    n = len(right)
    while i < m and j < n:
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

@timeit
def heap_sort(a):
    heap = Maxheap(a)
    return heap.sort()

@timeit
def builtin_sort(a):
    return sorted(a)

# mysort = heap_sort

# a_inv = [i for i in range(10, 0, -1)]
# quicksort(a_inv)
# insertion_sort(a_inv)
# print(mysort(a_inv))
# print(a_inv)

# a_repeat = [3,3,5,5,4,4,6]
# print(mysort(a_repeat))
# quicksort(a_repeat)
# insertion_sort(a_repeat)
# mysort(a_repeat)
# print(a_repeat)

# a_same = [1 for _ in range(10)]
# print(mysort(a_same))
# print(a_same)

def sort_compare():
    times = [10 ** i for i in range(1, 6)]
    merge = []
    quick = []
    heap = []
    insertion = []
    quick_cutoff = []
    for n in times:
        a = [random() for _ in range(n)]
        ans, t = merge_sort(a[:])
        merge.append(t)
        if n < 1e4 + 1:
            # print(n)
            ans, t = insertion_sort(a[:])
            insertion.append(t)
        ans, t = heap_sort(a[:])
        heap.append(t)
        ans, t = quick_sort(a[:])
        quick.append(t)
        ans, t = quick_sort_cutoff(a[:])
        quick_cutoff.append(t)
        # print(merge)
    for lst, name in zip([merge, quick, quick_cutoff, heap],
                         ['merge', 'quick', 'quick_cutoff', 'heap']):
        # print(lst)
        plt.plot(times, lst, label=str(name))
    # print(quick_cutoff)
    # print(heap)
    plt.plot(times[:4], insertion, label="insertion")
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.show()


# a = [random() for _ in range(10 ** 6)]
# start = clock()
# sorted(a)
# end = clock()
# print("Finished in: %.2fs" % (end - start))
# _, t = quick_sort_cutoff(a[:])
# print("Quicksort_cutoff finished in: %.2fs" % t)
# _, t = heap_sort(a[:])
# print("Heapsort finished in: %.2fs" % t)
# times = [10 ** i for i in range(5)]
# insert = []
# for n in times:
#     a = [random() for _ in range(n)]
#     _, t = insertion_sort(a[:])
#     insert.append(t)
# plt.plot(times, insert, label="insertion")
# plt.xscale('log')
# plt.yscale('log')
# plt.legend()
# plt.show()

def insertion_quick_compare():
    times = list(range(1, 21))
    insert_time = []
    quick_time = []
    for i in times:
        a = [random() for _ in range(i)]
        _, t = insertion_sort(a[:])
        insert_time.append(t)
        ans, t = quick_sort(a[:], False)
        quick_time.append(t)

    plt.plot(times, insert_time, label="insertion")
    plt.plot(times, quick_time, label="quick")

    plt.legend()
    plt.show()

sort_compare()