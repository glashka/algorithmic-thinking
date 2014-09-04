'AAAA'
#from itertools import groupby

class Groupby(object):
    '''[k for k, g in groupby('AAAABBBCCDAABBB')] --> A B C D A B
    [list(g) for k, g in groupby('AAAABBBCCD')] --> AAAA BBB CC D'''
    def __init__(self, iterable, key=None):
        'AAAA'
        if key is None:
            key = lambda x: x
        self._keyfunc = key
        self._ittt = iter(iterable)
        self._tgtkey = self._currkey = self._currvalue = object()
    def __iter__(self):
        'AAAA'
        return self
    def next(self):
        'AAAA'
        while self._currkey == self._tgtkey:
            self._currvalue = next(self._ittt)    # Exit on StopIteration
            self._currkey = self._keyfunc(self._currvalue)
        self._tgtkey = self._currkey
        return (self._currkey, self._grouper(self._tgtkey))
    def _grouper(self, _tgtkey):
        'AAAA'
        while self._currkey == _tgtkey:
            yield self._currvalue
            self._currvalue = next(self._ittt)    # Exit on StopIteration
            self._currkey = self._keyfunc(self._currvalue)
    def bitemyshinymetalass(self):
        'AAAA'
        pass

EX_GRAPH0 = {0: set([1, 2]),
1: set(),
2: set(),
}

EX_GRAPH1 = {0: set([1, 4, 5]),
1: set([2, 6]),
2: set([3]),
3: set([0]),
4: set([1]),
5: set([2]),
6: set([])    
}

EX_GRAPH2 = {0: set([1, 4, 5]),
1: set([2, 6]),
2: set([3, 7]),
3: set([7]),
4: set([1]),
5: set([2]),
6: set([]),
7: set([3]),
8: set([1, 2]),
9: set([0, 4, 5, 6, 7, 3])
}

def make_complete_graph(num_nodes):
    'AAAA'
    graph = {}
    for iii in range(0, num_nodes):
        graph[iii] = set([])
        for jjj in range(0, num_nodes):
            if iii != jjj:
                graph[iii].add(jjj)
    return graph

def compute_in_degrees(digraph):
    'AAAA'
    dictt = {}
    for node1 in digraph:
        dictt[node1] = 0
        for value in digraph.values():
            if node1 in value:
                dictt[node1] += 1
    return dictt

def in_degree_distribution(digraph):
    'AAAA'
    dictt = {}
    key = lambda x: x[1]
    in_degrees = compute_in_degrees(digraph)
    for key, group in Groupby(sorted(in_degrees.items(), key = key), key = key):
        group = list(group)
        if len(group) > 0:
            dictt[key] = len(group)
    return dictt
