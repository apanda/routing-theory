#!/usr/bin/env pypy
import networkx as nx
def CheckConnectivity(tables, links, size, xlate):
    #for origin in xrange(0, 4):
    #    for dest in xrange(origin + 1, 4):
    dest = 0
    for origin in xrange(1, size):
        #print str.format("Routing between {0} and {1}", origin, dest)
        visited = []
        visited_links = []
        current = origin
        inport = origin
        for_print = []
        while True:

            for_print.append(str(current))
            next_hop = tables[current][inport]
            edge = (min(xlate[current], xlate[next_hop]), max(xlate[current], xlate[next_hop]))
            dest_edge = (min(xlate[current], dest), max(xlate[current], dest))
            #print str.format("Attempting edge {0}", edge)
            if dest_edge in links and links[dest_edge]:
                #print "Going to destination"
                next_hop = dest
                break
            if edge[0] == edge[1] or ((edge in links) and links[edge]):
                #print str.format("Going from {1} (input port = {2}) to {0}", xlate[next_hop], xlate[current], xlate[inport])
                if next_hop == dest:
                    break
                if (next_hop, current) in visited:
                    #print ','.join(for_print)
                    return False
                visited_links = []
                visited.append((next_hop, current))
                inport = current
                current = next_hop
            else:
                #print str.format("Failed to go from {1} to {0}", xlate[next_hop], xlate[current])
                if edge in visited_links:
                    #print ','.join(for_print)
                    return False
                for_print.append(str(next_hop))
                visited_links.append(edge)
                inport = next_hop
        #print "Done"
    return True

def RoutesIterator(neighbors):
    route = [0 for x in xrange(0, len(neighbors))]
    carry = 0
    while carry == 0:
        yield { x: y for x, y in zip(neighbors, map(lambda idx: neighbors[idx], route))}
        carry = 1
        i = 0
        while carry == 1 and i < len(neighbors):
            carry = (route[i] + carry) / len(neighbors)
            route[i] = (route[i] + 1) % len(neighbors)
            i = i+1

def CombineRouteIterators(size, neighbors):
    routes = []
    for node in xrange(0,size):
       routes.append(filter(lambda tab: not any(map(lambda x: tab[x] == x, tab.keys())), RoutesIterator(neighbors[node])))
    current_route = [0 for i in  xrange(0, size)]
    carry = 0
    while carry == 0:
        yield map(lambda (r_idx, idx): routes[r_idx][idx], zip(xrange(0, size), current_route))
        carry = 1
        i = 1
        while carry == 1 and i < size:
            carry = (current_route[i] + carry) / len(routes[i])
            current_route[i] = (current_route[i] + 1) % len(routes[i])
            i = i + 1

import itertools
def CheckRoutingTable(table, size, clique, graph,  k, xlate):
    clique_len = len(clique)
    links = {i : True for i in clique}
    if k == 0:
        if not CheckConnectivity(table, links, size, xlate):
            return False
        else:
            return True
    remove = itertools.combinations(xrange(0, clique_len), k)
    for rem_links in remove:
        for rem_link in rem_links:
            links[clique[rem_link]] = False
            graph.remove_edge(*clique[rem_link])
        if nx.is_connected(graph):
            if not CheckConnectivity(table, links, size, xlate):
                #print str.format("Failed, k = {0}", k)
                for rem_link in rem_links:
                    #print str.format("Link: {0}", clique[rem_link])
                    graph.add_edge(*clique[rem_link])
                return False
        for rem_link in rem_links:
            graph.add_edge(*clique[rem_link])
            links[clique[rem_link]] = True
    return True

import sys
def CheckTables(tables, size, clique, graph, k, k_min, xlate):
    count = 0L
    max_so_far = -1
    for table in tables:
        count = count + 1
        if count % 1000000 == 0:
            print >>sys.stderr, str.format("Explored {0}", count)
        found = -1
        for k_temp in xrange(0, k + 1):
            val = CheckRoutingTable(table, size, clique, graph, k_temp, xlate)
            if val:
                found = k_temp
            else:
                break
        if found > max_so_far:
            max_so_far = found
        if found >= k_min:
            pass
            #print  str.format("{1}: {0}", table, found)
        return found

def GenerateTable(current, global_order, size):
    table = [0 for x in xrange(0, size)]
    for k,v in global_order.iteritems():
        table[k] = v
    table[0] = ((current) % (size - 1)) + 1
    table[current] = 0
    return table
def GenerateOrdering(size, clique):
    clique_nodest = filter(lambda x: x[0] != 0, clique)
    G = nx.Graph()
    G.add_nodes_from(xrange(1, size))
    G.add_edges_from(clique_nodest, capacity = 1.0)
    components = nx.connected_component_subgraphs(G)
    ordering = []
    for component in components:
        component_degrees = nx.degree(component)
        sorted_component = sorted(component_degrees.items(), key = lambda item: item[1])
        added = []
        current = sorted_component[0][0]
        while len(added) < len(component):
            if current not in ordering:
                added.append(current)
                ordering.append(current)
            neighbours = [edge[1] for edge in nx.edges(component, current)]
            neighbours = filter(lambda x: x not in ordering, neighbours)
            if len(neighbours) == 0:
                current = ordering[ordering.index(current) - 1]
                continue
            sorted_nbrs = sorted([(n, component_degrees[n]) for n in neighbours], key = lambda item: item[1])
            current = sorted_nbrs[0][0]
    return ordering
if __name__ == "__main__":
    #size = 8
    #clique = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(0,7), (0,2),(0,3),(0,4),(0,5),(0,6)]
    #degrees = [7, 2,3,3,3,3,3,1]
    #neighbours = {0:[0,1,2,3,4,5,6,7], 1:[0,1,2],2:[0,1,2,3],3:[0,2,3,4],4:[0,3,4,5],5:[0,4,5,6],6:[0,5,6,7],7:[0,6,7]}
    #clique = [(0,1),(0,3),(0,4),(0,7),(1,2),(2,3),(5,6),(6,7)]
    #neighbours = {0:[0,1,3,4,5],1:[0,1,2],2:[1,2,3],3:[0,2,3],4:[0,4],5:[5,6],6:[5,6,7],7:[0,6,7]}
    # PODC graph
    #clique = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(3,6),(3,7)]
    #neighbours = {0:[0,1],1:[0,1,2], 2:[1,2,3],3:[2,3,4,6,7], 4:[3,4,5], 5:[4,5,6],6:[3,5,6],7:[3,7]}
    # something
    #clique = [(0,1),(0,2),(0,4),(0,5),(1,2),(2,3),(3,4),(3,5),(4,5)]
    #neighbours = {0:[0,1,2,4,5], 1:[0,1,2],2:[0,1,2,3],3:[2,3,4,5],4:[0,3,4,5],5:[0,3,4,5]}

    #clique = [(0,1),(0,2),(0,4),(0,5),(1,2),(2,3),(2,5),(3,4),(4,5)]
    #neighbours = {0:[0,1,2,4,5], 1:[0,1,2],2:[0,1,2,3,5],3:[2,3,4],4:[0,3,4,5],5:[0,2,4,5]}
    #size = 6 
    size = int(sys.argv[1])
    from copy import deepcopy
    universe = list(itertools.combinations(xrange(0, size), 2))
    #clique.remove((0,1))
    #clique.remove((2,3))
    #clique.remove((4,5))
    #clique.remove((1,3))
    #eremov,((0,2))
    ##clique.remove((0,3))
    for i in xrange(size / 2, len(universe)):
        print >>sys.stderr, str.format("Looking at i = {0}", i)
        for edges in itertools.combinations(universe, i):
            clique = deepcopy(universe)
            for edge in edges:
                clique.remove(edge)
            G = nx.Graph()
            G.add_nodes_from(xrange(0, size))
            G.add_edges_from(clique, capacity = 1.0)
            if not nx.is_connected(G):
                continue
            mincut = min(map(lambda x: nx.min_cut(G, x[0], x[1]), itertools.combinations(xrange(0, size), 2)))

            global_order = {(x + 1): (((x+1) % (size - 1)) + 1) for x in xrange(0, size - 1)}
            routing_table = {x: GenerateTable(x, global_order, size) for x in xrange(1, size)}
            tested = 0
            passed = 0
            #xlate = {0:0,1:1, 2:3, 3:2, 4:4, 5:5}
            #ret = CheckTables([routing_table], size, clique, G, mincut - 1, len(clique) - 2, xlate)
            #tested = tested + 1
            #if ret >= mincut - 1:
            #    passed = passed + 1
            #    print str.format("{0} {1}", ret, xlate)
            #sys.exit(1)
            failed_any = False
            perm = GenerateOrdering(size, clique)
            xlate = {x: perm[x - 1] for x in  xrange(1, size)}
            xlate[0] = 0
            ret = CheckTables([routing_table], size, clique, G,  mincut - 1, mincut + 1, xlate)
            tested = tested + 1
            if ret >= mincut - 1:
                passed = passed + 1
                #print str.format("{0} {1}", ret, xlate)
            else:
                ordering = [xlate[k] for k in xrange(0, size)][1:]
                links = [(min(ordering[i], ordering[(i+1) % len(ordering)]), max(ordering[i], ordering[(i + 1) % len(ordering)])) for i in xrange(0, len(ordering))]
                existence = [(l in clique) for l in links]
                if all(existence):
                    print str.format("FAILURE {2} {3} {0} {1}", clique, [xlate[k] for k in xrange(0, size)], mincut, ret)
                    print >>sys.stderr, "Found failure"
                    failed_any = True
                else:
                    passed = passed + 1
            if failed_any:
                print str.format("Passed {0} out of {1}", passed, tested)

