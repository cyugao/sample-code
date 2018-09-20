from queue import Queue as Q
from heapq import heappop, heappush
from itertools import count
import time

import resource

import sys

import math


#### SKELETON CODE ####

## The Class that Represents the Puzzle

class PuzzleState(object):
    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0):

        if n * n != len(config) or n < 2:
            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []

        self.id = 0

        length = n * n

        for i, item in enumerate(self.config):

            if item == 0:
                self.blank_index = i
                self.blank_row = i // self.n
                self.blank_col = i % self.n

            self.id = self.id * length + item

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):
                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            target = self.blank_index - 1

            new_config = list(self.config)

            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            target = self.blank_index + 1

            new_config = list(self.config)

            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            target = self.blank_index - self.n

            new_config = list(self.config)

            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            target = self.blank_index + self.n

            new_config = list(self.config)

            new_config[self.blank_index], new_config[target] = new_config[target], new_config[self.blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:
                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:
                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:
                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:
                self.children.append(right_child)

        return self.children


# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters


GOAL_STATE_HASH = 6053444
nodes_expanded = 0
max_search_depth = 0
max_ram_usage = 0


def write_output(final_state: PuzzleState, duration, fp):
    path = []
    state = final_state
    while state:
        path.append(state.action)
        state = state.parent
    print("path_to_goal: %s" % list(reversed(path[:-1])),
          "cost_of_path: %s" % final_state.cost,
          "nodes_expanded: %s" % nodes_expanded,
          "search_depth: %s" % final_state.cost,
          "max_search_depth: %s" % max_search_depth,
          "running_time: %s" % duration,
          "max_ram_usage: %s" % (max_ram_usage / 1e6), sep='\n', file=fp)

def update_ram_usage():
    global max_ram_usage
    ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if ram > max_ram_usage:
        max_ram_usage = ram

def bfs_search(initial_state: PuzzleState):
    """BFS search"""

    global nodes_expanded, max_search_depth, max_ram_usage

    queue = Q()
    explored_and_frontier = {initial_state}

    queue.put(initial_state)
    while not queue.empty():
        # update_ram_usage()
        state: PuzzleState = queue.get()

        if hash(state) == GOAL_STATE_HASH:
            update_ram_usage()
            return state

        nodes_expanded += 1
        for child in state.expand():
            if child not in explored_and_frontier:
                explored_and_frontier.add(child)
                queue.put(child)
                if child.cost > max_search_depth:
                    max_search_depth = child.cost


def dfs_search(initial_state: PuzzleState):
    """DFS search"""

    global nodes_expanded, max_search_depth
    stack = [initial_state]
    explored_and_frontier = {initial_state}

    while stack:
        state = stack.pop()

        if hash(state) == GOAL_STATE_HASH:
            update_ram_usage()
            return state

        nodes_expanded += 1
        for child in reversed(state.expand()):
            if child not in explored_and_frontier:
                explored_and_frontier.add(child)
                stack.append(child)
                if child.cost > max_search_depth:
                    max_search_depth = child.cost


pq = []  # list of entries arranged in a heap
entry_finder = {}  # mapping of tasks to entries
REMOVED = None  # placeholder for a removed task
counter = count()     # unique sequence count


def add_task(task, priority=0):
    """Add a new task or update the priority of an existing task"""
    if task in entry_finder:
        remove_task(task)
    count = next(counter)
    entry = [priority, count, task]
    entry_finder[task] = entry
    heappush(pq, entry)


def remove_task(task):
    """Mark an existing task as REMOVED.  Raise KeyError if not found."""
    entry = entry_finder.pop(task)
    entry[-1] = REMOVED


def pop_task():
    """Remove and return the lowest priority task. Raise KeyError if empty."""
    while pq:
        priority, count, task = heappop(pq)
        if task is not REMOVED:
            del entry_finder[task]
            return task
    raise KeyError('pop from an empty priority queue')


def a_star_search(initial_state: PuzzleState):
    """A * search"""

    global nodes_expanded, max_search_depth

    add_task(initial_state, calculate_total_cost(initial_state))
    explored_and_frontier = {initial_state}

    while pq:
        state: PuzzleState = pop_task()

        if hash(state) == GOAL_STATE_HASH:
            update_ram_usage()
            return state

        nodes_expanded += 1
        for child in reversed(state.expand()):
            if child not in explored_and_frontier:
                explored_and_frontier.add(child)
                add_task(child, calculate_total_cost(child))
                if child.cost > max_search_depth:
                    max_search_depth = child.cost


def calculate_total_cost(state: PuzzleState):
    """calculate the total estimated cost of a state"""

    manhattan = sum(calculate_manhattan_dist(idx, value, state.n) for idx, value in enumerate(state.config))
    return manhattan + state.cost


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    if value == 0:
        return 0
    idx_x, idx_y = idx // n, idx % n
    value_x, value_y = value // n, value % n
    return abs(idx_x - value_x) + abs(idx_y - value_y)


# Main Function that reads in Input and Runs corresponding Algorithm

sm = sys.argv[1].lower()

begin_state = sys.argv[2].split(",")

begin_state = tuple(map(int, begin_state))

size = int(math.sqrt(len(begin_state)))

hard_state = PuzzleState(begin_state, size)

start = time.clock()

if sm == "bfs":

    state = bfs_search(hard_state)

elif sm == "dfs":

    state = dfs_search(hard_state)

elif sm == "ast":

    state = a_star_search(hard_state)

else:

    print("Enter valid command arguments !")

end = time.clock()

fp = open('output.txt', 'w')
write_output(state, end - start, fp)
fp.close()