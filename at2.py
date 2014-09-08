"""This is an implementations of BFS algorithm for week 2 of Algorithmic Thinking
"""

from collections import deque
import random

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
    after_attack = list()
    after_attack.append(largest_cc_size(ugraph))
    for attack_node in attack_order:
        del ugraph[attack_node]
        for node in ugraph.keys():
            ugraph[node] = ugraph[node] - {attack_node}
        after_attack.append(largest_cc_size(ugraph))
    return after_attack
