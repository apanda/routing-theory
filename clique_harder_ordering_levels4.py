#!/usr/bin/env pypy
import networkx as nx

def CheckConnectivity(tables, links, size, xlate):
    #for origin in xrange(0, 4):
    #    for dest in xrange(origin + 1, 4):
    dest = 0
    for origin in xrange(1, size):
        #print str.format("Routing between {0} and {1}", xlate[origin], dest)
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
                    print ','.join(for_print)
                    return False
                for_print.append(str(next_hop))
                visited_links.append(edge)
                inport = next_hop
        #print "Done"
        #print 
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
def CheckRoutingTable(table, size, clique, graph, k, xlate):
    clique_len = len(clique)
    links = {i : True for i in clique}
    if k == 0:
        if not CheckConnectivity(table, links, size, xlate):
            return (False, [])
        else:
            return True
    remove = itertools.combinations(xrange(0, clique_len), k)
    for rem_links in remove:
        for rem_link in rem_links:
            #print str.format("Failing {0}", clique[rem_link])
            links[clique[rem_link]] = False
            graph.remove_edge(*clique[rem_link])
        if nx.is_connected(graph):
            if not CheckConnectivity(table, links, size, xlate):
                #print str.format("Failed, k = {0}", k)
                for rem_link in rem_links:
                    #print str.format("Link: {0}", clique[rem_link])
                    graph.add_edge(*clique[rem_link])
                #print str.format("Failing with failed links: {0}", map(lambda a: clique[a], rem_links))
                return (False, map(lambda a: clique[a], rem_links))
        for rem_link in rem_links:
            graph.add_edge(*clique[rem_link])
            links[clique[rem_link]] = True
    return True

import sys
def CheckTables(tables, size, clique, graph, k, k_min, xlate):
    count = 0L
    max_so_far = -1
    min_cut_so_far = len(clique)
    min_edges = []
    first_fail = -1
    assert len(tables) == 1
    for table in tables:
        count = count + 1
        if count % 1000000 == 0:
            print >>sys.stderr, str.format("Explored {0}", count)
        found = -1
        for k_temp in xrange(0, k + 1):
            val = CheckRoutingTable(table, size, clique, graph, k_temp, xlate)
            if val == True:
                found = k_temp
            else:
                if min_cut_so_far > k_temp:
                    min_edges = val[1]
                    min_cut_so_far = k_temp
                break
        if found > max_so_far:
            max_so_far = found
            #print >>sys.stderr, str.format("Maximum so far {0}", found)
        if found >= k_min:
            pass
            #print  str.format("{1}: {0}", table, found)
        return (found, min_edges)
def GenerateTable(current, global_order, size):
    table = [0 for x in xrange(0, size)]
    for k,v in global_order.iteritems():
        table[k] = v
    table[0] = ((current) % (size - 1)) + 1
    table[current] = 0
    return table

if __name__ == "__main__":
    size = int(sys.argv[1])
    from copy import deepcopy
    #if len(sys.argv) > 2:
    #    universe = eval(sys.argv[2])
    #else:
    universe = list(itertools.combinations(xrange(0, size), 2))
    global_order = {(x + 1): (((x+1) % (size - 1)) + 1) for x in xrange(0, size - 1)}
    routing_table = {x: GenerateTable(x, global_order, size) for x in xrange(1, size)}
    del global_order
    use_input = True
    if len(sys.argv) > 2:
        start = int(sys.argv[2])
    else:
        start = len(universe)
    for i in xrange(start, 1, -1):
        print >>sys.stderr, str.format("Looking at i = {0}", i)
        failed_any = False
        tested_any = False
        for edges in itertools.combinations(universe, i):
            clique = deepcopy(universe)
            for edge in edges:
                clique.remove(edge)
            neighbours = {x:range(0,size) for x in xrange(0,size)}

            G = nx.Graph()
            G.add_nodes_from(xrange(0, size))
            G.add_edges_from(clique, capacity = 1.0)
            if not nx.is_connected(G):
                continue
            tested_any = True
            mincut = min(map(lambda x: nx.min_cut(G, x[0], x[1]), itertools.combinations(xrange(0, size), 2)))
            levels = []
            if use_input and len(sys.argv) > 3:
                global_order = [eval(sys.argv[3])]
                use_input = False
            else:
                lengths = nx.all_pairs_dijkstra_path_length(G)
                to_dest = {x: lengths[x][0] for x in xrange(0, size)}
                sorted_dest = sorted(to_dest.iteritems(), key=lambda x: x[1])
                max_dist = sorted_dest[-1][1]
                for dists in xrange(0, max_dist + 1):
                    levels.append(map(lambda x: x[0], filter(lambda x: x[1] == dists, sorted_dest)))
                orders = itertools.product(*map(itertools.permutations, levels))
                global_order = map(lambda x: list(itertools.chain(*x)), orders)
            #print >>sys.stderr, levels
            ret = map(lambda go: CheckTables([routing_table], size, clique, G,  mincut, mincut + 2, go), global_order)
            if any(map(lambda a: a[0] >= mincut - 1, ret)):
                pass
                #for cut, order in zip(map(lambda g:g[1], ret), global_order):
                #    if len(cut) > 0:
                #        print str.format("{3} {0} {1} {2}", clique, order, cut, mincut)
            else:
                for cut, order in zip(map(lambda g:g[1], ret), global_order):
                    print str.format("{0} {1} {2}", clique, order, cut)
                print >>sys.stderr, "Found failure"
                failed_any = True
                break
        if tested_any and not failed_any:
            pass
            #break

