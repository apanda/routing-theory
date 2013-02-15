import sys
import networkx as nx
from itertools import combinations
def route(graph, dest, order):
    table = {order[x]: order[(x + 1)%len(order)] for x in xrange(0, len(order))}
    for src in order:
        current = src
        incident = src
        used = {e: False for e in graph.edges()}
        for e in graph.edges():
            used[(e[1], e[0])] = False
        while current != dest:
            incident = table[incident]
            if (current, dest) in used:
                (current, incident) = (dest, current)
                break
            if (current, incident) in used:
                if used[(current, incident)]:
                    break
                used[(current, incident)] = True
                (current, incident) = (incident, current)
        if current != dest:
            print >>sys.stderr, str.format("Src = {0}", src)
            return False
    return True
if len(sys.argv) < 5:
    print str.format("{0} <topo> <order> <k> <dest>", sys.argv[0])
    sys.exit(1)
topo = eval(sys.argv[1])
order = eval(sys.argv[2])
k = int(sys.argv[3])
dest = int(sys.argv[4])
print str.format("k = {0} dest = {1} order = {2}", k, dest, order)
graph = nx.Graph()
graph.add_edges_from(topo)
for edges in combinations(graph.edges(), k):
    copy = graph.copy()
    copy.remove_edges_from(edges)
    if not route(copy, dest, order):
        print "FAILED"
        print str.format("Order = {0} Graph = {1} Removed = {2}", order, copy.edges(), edges)
        sys.exit(1)
    else:
        print "PASSED"


