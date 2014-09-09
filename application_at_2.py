
# coding: utf-8

# In[1]:

"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
from collections import deque
import matplotlib.pyplot as pyplot
get_ipython().magic(u'matplotlib inline')
import matplotlib.pylab as pylab

# CodeSkulptor import
#import simpleplot
#import codeskulptor
#codeskulptor.set_timeout(60)

# Desktop imports
#import matplotlib.pyplot as plt


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


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


# In[2]:

NETWORK_GRAPH = load_graph(NETWORK_URL)


# In[3]:

def generate_er_undirected_graph(num_nodes, probability):
    """Generates random undirected graph using ER algorithm
    """
    result = {}
    if num_nodes == 0:
        return result
    for node1 in range(0, num_nodes):
        if node1 not in result:
            result[node1] = set()
        for node2 in range(0, num_nodes):
            if node2 not in result:
                result[node2] = set()
            if (random.random() < probability and node1 != node2):
                result[node1].add(node2)
                result[node2].add(node1)
    return result


# In[4]:

class UPATrial:
    """
    Simple class to encapsulate optimized trials for UPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
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


# In[5]:

def generate_upa_graph(num_nodes, iter_nodes):
    """
    Generates graph by UPA algorithm where num_nodes is a total number of nodes
    and iter_nodes is a number of edges added on each iteration
    """
    result = make_complete_graph(iter_nodes)
    upa = UPATrial(iter_nodes)
    if num_nodes <= iter_nodes:
        return result
    for step in range(iter_nodes, num_nodes):
        nodes_to_be_added = upa.run_trial(iter_nodes)
        result[step] = nodes_to_be_added
        for node in nodes_to_be_added:
            result[node].add(step)
    return result


# In[6]:

ER_GRAPH = generate_er_undirected_graph(1347, 0.0017164333)


# In[7]:

UPA_GRAPH = generate_upa_graph(1347, 2)


# In[8]:

def random_order(graph):
    nodes = graph.keys()
    random.shuffle(nodes)
    return nodes


# In[9]:

def bfs_visited(ugraph, start_node):
    """Takes the undirected graph ugraph and the node start_node and returns the set 
    consisting of all nodes that are visited by a breadth-first search that starts at start_node
    """
    visited = set()
    visited.add(start_node)
    queue = deque()
    queue.append(start_node)
    while len(list(queue)) > 0:
        node = queue.pop()
        for neighbour in ugraph[node]:
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)
    return visited

def cc_visited(ugraph):
    """Takes the undirected graph ugraph and returns a list of sets, where each set consists of all the nodes 
    (and nothing else) in a connected component, and there is exactly one set in the list for each connected 
    component in ugraph and nothing else
    """
    remaining = set(ugraph.keys())
    connected = list()
    while len(remaining) > 0:
        component = bfs_visited(ugraph, random.sample(remaining, 1)[0])
        connected.append(component)
        remaining = remaining - component
    return connected

def largest_cc_size(ugraph):
    """Takes the undirected graph ugraph and returns the size (an integer) of the largest connected component in ugraph
    """
    connected = cc_visited(ugraph)
    component_size = 0
    for component in range(0, len(connected)):
        if len(connected[component]) > component_size:
            component_size = len(connected[component])
    return component_size

def compute_resilience(ugraph, attack_order):
    """Takes the undirected graph ugraph, a list of nodes attack_order and iterates through the nodes in attack_order 
    For each node in the list, the function removes the given node and its edges from the graph and then computes 
    the size of the largest connected component for the resulting graph.
    """
    after_attack = dict()
    tick = 0
    after_attack[tick] = largest_cc_size(ugraph)
    for attack_node in attack_order:
        tick += 1
        del ugraph[attack_node]
        for node in ugraph.keys():
            ugraph[node] = ugraph[node] - {attack_node}
        after_attack[tick] = largest_cc_size(ugraph)
    return after_attack


# In[10]:

NETWORK_RESILIENCE = compute_resilience(NETWORK_GRAPH, random_order(NETWORK_GRAPH))
ER_RESILIENCE = compute_resilience(ER_GRAPH, random_order(ER_GRAPH))
UPA_RESILIENCE = compute_resilience(UPA_GRAPH, random_order(UPA_GRAPH))


# In[15]:

pylab.rcParams['figure.figsize'] = 16, 12

pyplot.xlabel('Number of nodes removed')
pyplot.ylabel('Size of the largest connect component')
pyplot.title('Comparison of networks resilience')
pyplot.plot([x for (x, y) in NETWORK_RESILIENCE.items()], [y for (x, y) in NETWORK_RESILIENCE.items()], 'r.', label = 'NETWORK')
pyplot.plot([x for (x, y) in ER_RESILIENCE.items()], [y for (x, y) in ER_RESILIENCE.items()], 'g.', label='ER, n=1347, p=0.0017164333')
pyplot.plot([x for (x, y) in UPA_RESILIENCE.items()], [y for (x, y) in UPA_RESILIENCE.items()], 'b.', label='UPA, n=1347, m=2')
pyplot.legend()

pyplot.show()


# In[ ]:



