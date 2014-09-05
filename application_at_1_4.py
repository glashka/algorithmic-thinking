"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""

# general imports
import random
import matplotlib.pyplot as pyplot
import matplotlib.pylab as pylab
%matplotlib inline
import urllib2


class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    
def make_complete_graph(num_nodes):
    """
    Makes complete graph with a given number of nodes
    """
    graph = {}
    for node1 in range(0, num_nodes):
        graph[node1] = set([])
        for node2 in range(0, num_nodes):
            if node1 != node2:
                graph[node1].add(node2)
    return graph
    
def generate_dpa_graph(num_nodes, iter_nodes):
    """
    Generates graph by DPA algorithm where num_nodes is a total number of nodes
    and iter_nodes is a number of edges added on each iteration
    """
    result = make_complete_graph(iter_nodes)
    dpa = DPATrial(iter_nodes)
    if num_nodes <= iter_nodes:
        return result
    for step in range(iter_nodes, num_nodes):
        result[step] = dpa.run_trial(iter_nodes)
#        for neighbour in neighbours:
#            result[step].add(neighbour)
    return result

dpa_graph = generate_dpa_graph(27770, 13)

def compute_in_degrees(digraph):
    """Computes indegrees of a digraph.
    """
    result = {}
    for key in digraph.iterkeys():
        result[key] = 0
    for vset in digraph.itervalues():
        for val in vset:
            result[val] += 1
    return result

def in_degree_distribution(digraph):
    """Computes indegree distribution of a digraph.
    """
    indeg = compute_in_degrees(digraph)
    result = {}
    sum_indegrees = 0
    for val in indeg.itervalues():
        if val not in result:
            result[val] = 0
        result[val] += 1
        sum_indegrees += 1
    for val in result.iterkeys():
        result[val] = result[val] / float(sum_indegrees)
    return result

"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

citation_graph = load_graph(CITATION_URL)

dpa_distribution = in_degree_distribution(dpa_graph)
citation_distribution = in_degree_distribution(citation_graph)

pylab.rcParams['figure.figsize'] = 16, 12

pyplot.xscale('log')
pyplot.yscale('log')
pyplot.xlabel('in-degree')
pyplot.ylabel('share of nodes')
pyplot.title('DPA random graph vs. citation graph in-degree normalized distribution')
pyplot.plot([x for (x, y) in dpa_distribution.items()], [y for (x, y) in dpa_distribution.items()], 'r.', label='DPA')
pyplot.plot([x for (x, y) in citation_distribution.items()], [y for (x, y) in citation_distribution.items()], 'g.', label='Citation')
pyplot.legend()

pyplot.show()

pylab.rcParams['figure.figsize'] = 16, 12

pyplot.xscale('log')
pyplot.yscale('log')
pyplot.xlabel('in-degree')
pyplot.ylabel('share of nodes')
pyplot.title('DPA random graph in-degree normalized distribution')
pyplot.plot([x for (x, y) in dpa_distribution.items()], [y for (x, y) in dpa_distribution.items()], 'r.', label='DPA')

pyplot.show()

