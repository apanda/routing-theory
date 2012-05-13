import sys
import networkx as nx
from time import time
from copy import deepcopy
from itertools import permutations, combinations
stop = False
explored = 0
while not stop:
  explored += 1
  nodes = 8
  degree = 3
  G  = nx.random_regular_graph(degree, nodes)
  nx.set_edge_attributes(G, 'capacity', {k : 1.0 for k in G.edges_iter()})
  umoded_graph = nx.Graph.copy(G)
  try:
    source = nx.periphery(G)[0]
  except:
    continue
  diameter = nx.diameter(G)
  distances = nx.single_source_dijkstra(G, source)
  target = max(distances[1], key=lambda k:distances[0][k])
  nbrs = G.neighbors(source)
  G.graph['source'] = source
  G.graph['dest'] = target
  G.node[source]['source'] = True
  G.node[target]['target'] = True
  paths = []
  mincut = min(map(lambda x: nx.min_cut(G, x[0], x[1]), combinations(xrange(0, nodes), 2)))
  for ordering in permutations(nbrs):
    G = nx.Graph.copy(umoded_graph)
    del paths[:]
    for order in ordering:
      if not nx.has_path(G, order, target):
        break
      else:
        path = nx.dijkstra_path(G, order, target)
        paths.append(path)
        edges = [(path[i], path[i + 1]) for i in xrange(0, len(path) - 1)]
        G.remove_edges_from(edges)
    if len(paths) >= mincut:
      break
  if len(paths) < mincut:
    print str.format("Min-cut = {0}", mincut)
    print str.format("Neighbors: {0}", nbrs)
    for ordering in permutations(nbrs):
      G = nx.Graph.copy(umoded_graph)
      del paths[:]
      for order in ordering:
        if not nx.has_path(G, order, target):
          print str.format("For ordering {0}, no ordering for {1}", ordering, order)
          break
        else:
          path = nx.dijkstra_path(G, order, target)
          paths.append(path)
          edges = [(path[i], path[i + 1]) for i in xrange(0, len(path) - 1)]
          G.remove_edges_from(edges)
      if len(paths) >= degree:
        break
    stop = True
    print str.format("Source = {0} Target = {1}", source, target)
    nx.write_dot(umoded_graph, 'graph.dot')
    print str.format("FAILURE in {0}", explored)
    print paths
