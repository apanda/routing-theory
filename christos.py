import sys
import networkx as nx
from time import time
from copy import deepcopy
stop = False
while not stop:
  nodes = 8
  degree = 3
  G  = nx.random_regular_graph(degree, nodes)
  nx.set_edge_attributes(G, 'capacity', {k : 1.0 for k in G.edges_iter()})
  umoded_graph = nx.Graph.copy(G)

