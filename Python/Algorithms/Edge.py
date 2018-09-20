from functools import total_ordering

@total_ordering
class Edge(object):
    """docstring for Edge"""

    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight

    def verts(self):
        return self.u, self.v

    def either(self):
        return self.u

    def other(self, w):
        if w == self.u:
            return self.v
        if w == self.v:
            return self.u
        else:
            return KeyError

    def __lt__(self, other):
        return self.weight < other.weight

    def __eq__(self, other):
        return self.weight == other.weight

    def __str__(self):
        return "%d-%d: %.1f" % (self.u, self.v, self.weight) 

if __name__ == '__main__':
    e1 = Edge(1,3,5)
    e2 = Edge(2,4,6)
    print(e1 < e2)