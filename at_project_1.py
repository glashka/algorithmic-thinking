"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2

# Set timeout for CodeSkulptor if necessary
#import codeskulptor
#codeskulptor.set_timeout(20)

import matplotlib.pyplot as pyplot
import matplotlib.pylab as pylab

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

def in_degree_norm_distribution(digraph):
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

digraph1 = generate_er_directed_graph(3000, 0.3)
digraph2 = generate_er_directed_graph(3000, 0.5)
digraph3 = generate_er_directed_graph(3000, 0.7)

distribution1 = in_degree_distribution(digraph1)

distribution2 = in_degree_distribution(digraph2)

distribution3 = in_degree_distribution(digraph3)

citation_distribution = in_degree_distribution(citation_graph)

pylab.rcParams['figure.figsize'] = 16, 12

pyplot.xscale('log')
pyplot.yscale('log')
pyplot.xlabel('in-degree')
pyplot.ylabel('share of nodes')
pyplot.title('Comparison of in-degree normalized distributions for ER random graphs and citation graph')
pyplot.plot([x for (x, y) in distribution1.items()], [y for (x, y) in distribution1.items()], 'r.', label='ER, p = 0.3')
pyplot.plot([x for (x, y) in distribution2.items()], [y for (x, y) in distribution2.items()], 'g.', label='ER, p = 0.5')
pyplot.plot([x for (x, y) in distribution3.items()], [y for (x, y) in distribution3.items()], 'b.', label='ER, p = 0.7')
pyplot.plot([x for (x, y) in citation_distribution.items()], [y for (x, y) in citation_distribution.items()], 'y.', label='citation graph')
pyplot.legend()

pyplot.show()

#%matplotlib inline

pylab.rcParams['figure.figsize'] = 16, 12

pyplot.xscale('log')
pyplot.yscale('log')
pyplot.xlabel('in-degree')
pyplot.ylabel('share of nodes')
pyplot.title('In-degree normalized distribution')
pyplot.plot([x for (x, y) in citation_distribution.items()], [y for (x, y) in citation_distribution.items()], 'r.')

pyplot.show()
