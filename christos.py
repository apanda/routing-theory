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
  source = nx.periphery(G)[0]
  diameter = nx.diameter(G)
  distances = nx.single_source_dijkstra(G, source)
  target = max(distances[1], key=lambda k:distances[0][k])
  paths = []
  routing_tables = {source:{}, target:{}}
  nodes_visited = set()
  print "-=-=-=-=-=-=-=-=-"
  for path in nx.all_shortest_paths(G, source=source, target=target):
    if not any(map(lambda a: a in nodes_visited, path[1:-1])):
      nodes_visited.update(path[1:-1])
      paths.append(path)
    else:
      print nodes_visited
      print path
      #stop = True
  print len(paths)
  if len(paths) < 3:
    print [p for p in nx.all_shortest_paths(umoded_graph, source=source, target=target)]
    print G.degree()
    stop = True
  #if len(paths) != degree:
  #  cut = nx.min_cut(umoded_graph, source, target)
  #  print str.format("Fewer than {0} paths; min-cut = {1}", degree, cut)
  #  G = nx.Graph.copy(umoded_graph)
  #  nbr = G.neighbors(source)
  #  unvisited_node = filter(lambda n: not any(map(lambda p: n in p, paths)), nbr)
  #  print str.format("Seed = {0}", seed)
  #  print paths
  #  print str.format("Unvisited = {0}", unvisited_node)
  #  print "== Original =="
  #  print nx.dijkstra_path(G, unvisited_node[0], target)
  #  for path in paths:
  #    edges = [(path[i], path[i + 1]) for i in xrange(0, len(path) - 1)]
  #    for i in xrange(1, len(path) - 1):
  #      if path[i] not in routing_tables:
  #        routing_tables[path[i]] = {}
  #      routing_tables[path[i]][path[i - 1]] = path[i + 1]
  #    G.remove_edges_from(edges)
  #    if nx.has_path(G, source, target):
  #      print str.format("== After path {0} ==", path)
  #      print nx.dijkstra_path(G, unvisited_node[0], target)
  #    else:
  #      print str.format("== After path {0} ==", path)
  #      print "No path"
  #      print [p for p in nx.all_shortest_paths(umoded_graph, source=source, target=target)]
  #      print str.format("Source: {0} Target: {1}", source, target)
  #      nx.write_dot(umoded_graph, 'graph.dot')
  #      break
  #  if cut == degree:
  #    stop = True
  #else:
  #  for i in xrange(0, len(paths) - 1):
  #    routing_tables[source][paths[i][1]] = paths[i + 1][1]
  #  #print routing_tables[source]
  #  #print paths
  #  for i in sorted(routing_tables.iterkeys()):
  #    for ingress, egress in sorted(routing_tables[i].iteritems(), key=lambda a: a[0]):
  #      pass
  #      #print str.format("{2}    {0}    {1}", ingress, egress, i)
