import sys
from copy import deepcopy

# formulation: norvig.com/sudoku.html

rows = 'ABCDEFGHI'
cols = '123456789'

cart = lambda row, col: [r + c for r in row for c in col]  # cartesian

squares = cart(rows, cols)
groups = ([cart(rows, c) for c in cols] +
          [cart(r, cols) for r in rows] +
          [cart(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')])
units = dict((s, [u for u in groups if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s], [])) - set([s]))
             for s in squares)
unknown = [str(i) for i in range(1, 10)]


class Sudoku(object):

    def __init__(self, board, fp):
        self.domain = {key: {value} if value != '0' else set(unknown)
                       for key, value in zip(squares, board)}
        self.arcs = peers
        self.count = {i: set() for i in range(10)}
        # self.display()
        self.AC3()
        if self.solved():
            print(str(self) + " AC3", file=fp)
        else:
            # classify by number of elements in its domain
            # self.display()
            for loc in squares:
                num = len(self.domain[loc])
                self.count[num].add(loc)
            self.count[0] = self.count[1] # 0 stands for assigned variables
            self.count[1] = set()
            self.mrv_next_loc = None
            self.next_mrv(2)

            self.search()
            if len(self.count[0]) == 81:
                print(str(self) + " BTS", file=fp)
            else:
                print("Failed to solve: str(self)")

    def next_mrv(self, start=1):
        j = start
        while j < 10:
            if not self.count[j]:  # empty
                j += 1
            else:
                self.mrv_next_loc = next(iter(self.count[j]))
                # self.mrv_next_loc = sorted(self.count[j])[0]
                return

    def solved(self):
        return all((len(d) == 1 for d in self.domain.values()))

    def AC3(self):
        queue = [(i, j) for i, i_nbr in self.arcs.items() for j in i_nbr]
        while queue:
            i, j = queue.pop()
            if self.revise(i, j):
                if not self.domain[i]:
                    return False
                for k in self.arcs[i] - {j}:
                    queue.append((k, i))

    def revise(self, j, i):
        flag = False
        if len(self.domain[i]) == 1:
            x = next(iter(self.domain[i]))  # get the only element
            if x in self.domain[j]:
                self.domain[j].remove(x)
                flag = True
        return flag

    def search(self, mrv=True):
        """
        :param mrv: minimum remaining values
        :return: True if succeed else False
        """
        # print(len(self.count[1]))
        if len(self.count[0]) == 81:
            return True
        # try assigning values to next cell with mrv
        domain = deepcopy(self.domain)
        count = deepcopy(self.count)
        self.next_mrv()
        loc = self.mrv_next_loc
        values = domain[loc]
        domain_size = len(domain[loc])
        for val in values:
            self.domain[loc] = {val}
            self.count[domain_size].remove(loc)
            self.count[0].add(loc)
            # propagate -- modify nbrs
            for nbr in peers[loc]:
                if val in self.domain[nbr]:
                    size = len(self.domain[nbr])
                    if size == 1:  # fail!
                        break  # skip search
                    self.count[size].remove(nbr)
                    self.count[size-1].add(nbr)
                    self.domain[nbr].remove(val)
            else:
                # self.display()
                result = self.search()
                if result:
                    return True

            # remove assignment
            self.domain = deepcopy(domain)
            self.count = deepcopy(count)

    def __str__(self):
        return ''.join((str(next(iter(self.domain[loc]))) if len(self.domain[loc]) == 1 else '0' for loc in squares))

    def display(self):
        "Display these values as a 2-D grid."
        width = 1 + max(len(self.domain[s]) for s in squares)
        line = '+'.join(['-' * (width * 3)] * 3)
        for r in rows:
            print(''.join(''.join(self.domain[r+c]).center(width) + ('|' if c in '36' else '')
                    for c in cols))
            if r in 'CF':
                print(line)
        print()

board_str = sys.argv[1]
fp = open('output.txt', 'w')
my_board = Sudoku(board_str, fp=fp)
fp.close()
