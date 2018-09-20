from MaxPQ import MaxPQ
from random import randint
from random import shuffle


class Search(object):
    """docstring for Search"""
           

    def __init__(self, v, w, max_cap):
        self.n = len(v)
        self.perm = list(range(self.n))
        self.max_cap = max_cap
        self.cur_max = 0
        self.deque = []
        
        self.cur_best_choice = set()
        self.rank = sorted(range(self.n), key=lambda pos: v[pos] / w[pos], reverse=True)

        SHUFFLE = False
        if SHUFFLE:
            # shuffle(self.perm)
            self.v = [v[i] for i in self.perm]
            self.w = [w[i] for i in self.perm]
        else:
            self.v = [v[i] for i in self.rank]
            self.w = [w[i] for i in self.rank]
        self.idx_sort_by_weight = sorted(range(self.n), key=lambda pos: self.w[pos])

    def bound(self, pos, cap_remain):
        # rank = [i for i in self.rank if i >= pos]
        cur_cap = 0
        cur_val = 0

        j = pos
        while j < self.n:
            if cur_cap + self.w[j] <= cap_remain:
                cur_cap += self.w[j]
                cur_val += self.v[j]
                j += 1
            else:
                break
        if j < self.n:
            # print(cur_cap)
            cur_val += self.v[j] / self.w[j] * (cap_remain - cur_cap)
        return cur_val

    def greedy(self):
        cur_cap = 0
        cur_val = 0
        choice_set = set()
        for j in range(self.n):
            weight = cur_cap + self.w[j]
            if  weight <= self.max_cap:
                cur_cap = weight
                cur_val += self.v[j]
                choice_set.add(j)
            if weight == self.max_cap:
                break
        return cur_val, choice_set

    def dfs(self, print_greedy=False):
        print("Size:", self.n)
        self.cur_max, self.cur_best_choice = self.greedy()
        if print_greedy:
            print("Greedy solution:")
            print((self.cur_max, self.cur_best_choice))
        val, choice = self.random_choice(500)
        print("Random:", val, choice)
        if val > self.cur_max:
            self.cur_max, self.cur_best_choice = val, choice
        self.deque.append((0, self.max_cap, 1, set()))
        self.deque.append((self.v[0], self.max_cap - self.w[0], 1, {0}))
        while self.deque:
            # pos: next position to be examined
            value, room, pos, choice_set = self.deque.pop()
            # if pos % 50 == 0:
                # print(pos)
            # examing current node
            if pos == self.n or room == 0:
                # nothing to expand
                if value > self.cur_max:
                    # update
                    self.cur_max = value
                    self.cur_best_choice = choice_set
                continue
            # bound
            max_v_remain = self.bound(pos, room)
            if value + max_v_remain <= self.cur_max:
                # branch
                continue
            self.deque.append((value, room, pos+1, choice_set))
            if room >= self.w[pos]:
                self.deque.append((value + self.v[pos], room - self.w[pos], pos+1, choice_set.union({pos})))
        return self.cur_max, self.cur_best_choice

    def random_choice(self, times):
        max_val = 0
        best_choice_set = set()
        for _ in range(times):
            cur_val = 0
            cur_cap = 0
            choice_set = set()
            count = 0
            while cur_cap < self.max_cap:
                i = randint(0, self.n - 1)
                if i in choice_set:
                    continue
                if cur_cap + self.w[i] <= self.max_cap:
                    cur_val += self.v[i]
                    cur_cap += self.w[i]
                    choice_set.add(i)
                else:
                    if count == 5:
                        break
                    count += 1
            for i in self.idx_sort_by_weight:
                if i in choice_set:
                    continue
                if cur_cap + self.w[i] > self.max_cap:
                    break
                else:
                    cur_cap += self.w[i]
                    cur_val += self.v[i]
                    choice_set.add(i)
            if cur_val > max_val:
                max_val = cur_val
                best_choice_set = choice_set
        return max_val, best_choice_set


    def update(self, value, room, pos, choice_set):
        # update or return estimate
        if pos == self.n or room == 0:
        # nothing to expand
            if value > self.cur_max:
                # update
                self.cur_max = value
                self.cur_best_choice = choice_set
            return -1

        estimate = self.bound(pos, room) + value
        if estimate < self.cur_max:
            return -1
        return estimate

    def best_first(self, print_greedy=False):
        # obtain a greedy solution first
        self.cur_max, self.cur_best_choice = self.greedy()
        if print_greedy:
            print("Greedy solution:")
            print((self.cur_max, self.cur_best_choice))
        pq = MaxPQ(self.n)
        first_estimate = self.bound(0, self.max_cap)
        pq.insert((first_estimate, 0, self.max_cap, 0, set()))
        while not pq.isEmpty():
            # pos: next position to be examined
            _, value, room, pos, choice_set = pq.extract_max()
            choice0 = (value, room, pos+1, choice_set)
            # print(choice0)
            choice1 = (value + self.v[pos], room - self.w[pos], pos+1, choice_set.union({pos}))
            estimate0 = self.update(*choice0)
            if estimate0 != -1:
                pq.insert((estimate0, ) + choice0)
            if choice1[1] >= 0:
                estimate1 = self.update(*choice1)
                if estimate1 != -1:
                    pq.insert((estimate1, ) + choice1)
        return self.cur_max, self.cur_best_choice


def solve(file):
    fp = open(file)
    firstline = fp.readline().split()
    cap = int(firstline[0])
    n = int(firstline[1])
    vs = [None] * n
    ws = [None] * n
    for i in range(0, n):
        line = fp.readline()
        vw = line.split()
        vs[i] = int(vw[0])
        ws[i] = int(vw[1])
    # print(vs[:10])
    kp = Search(vs, ws, cap)
    # result = kp.dfs()
    result = kp.best_first()
    return result

def test_dfs():
    vs = [45, 48, 35]
    ws = [5, 8, 3]
    cap = 10

    kp = Search(vs, ws, cap)
    # print(kp.best_first())

if __name__ == '__main__':
    pass
    # print(solve("knapsack2.txt"))
    # print("Optimal solution:")
    # print(solve("knapsack_small.txt"))

