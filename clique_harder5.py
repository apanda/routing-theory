#!/usr/bin/env pypy
import networkx as nx
def CheckConnectivity(tables, links, size):
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
            edge = (min(current, next_hop), max(current, next_hop))
            #print str.format("Attempting edge {0}", edge)
            if edge[0] == edge[1] or ((edge in links) and links[edge]):
                if next_hop == dest:
                    break
                if next_hop in visited:
                    #print ','.join(for_print)
                    return False
                visited_links = []
                visited.append(next_hop)
                inport = current
                current = next_hop
            else:
                if edge in visited_links:
                    #print ','.join(for_print)
                    return False
                for_print.append(str(next_hop))
                visited_links.append(edge)
                inport = next_hop
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

def CheckRoutingTable(table, size, clique, graph, degrees, k):
    clique_len = len(clique)
    links = {i : True for i in clique}
    import itertools
    remove = itertools.combinations(xrange(0, clique_len), k)
    removed_degree = [0 for x in xrange(0, size)]
    for rem_links in remove:
        for rem_link in rem_links:
            links[clique[rem_link]] = False
            graph.remove_edge(*clique[rem_link])
            removed_degree[clique[rem_link][0]] = removed_degree[clique[rem_link][0]] + 1
            removed_degree[clique[rem_link][1]] = removed_degree[clique[rem_link][1]] + 1
        if nx.is_connected(graph):
            for rem_link in rem_links:
                graph.add_edge(*clique[rem_link])
            if not CheckConnectivity(table, links, size):
                return False
        for rem_link in rem_links:
            graph.add_edge(*clique[rem_link])
            removed_degree[clique[rem_link][0]] = removed_degree[clique[rem_link][0]] - 1
            removed_degree[clique[rem_link][1]] = removed_degree[clique[rem_link][1]] - 1
            links[clique[rem_link]] = True
    return True

import sys
def CheckTables(tables, size, clique, graph, degrees, k):
    count = 0L
    for table in tables:
        count = count + 1
        if count % 1000000 == 0:
            print >>sys.stderr, str.format("Explored {0}", count)
        k_temp = k
        while CheckRoutingTable(table, size, clique, graph, degrees, k_temp) and k_temp > 0:
            k_temp = k_temp -1
        if k_temp == 0:
            print  str.format("{0}", table)

if __name__ == "__main__":
    #clique = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(0,7), (0,2),(0,3),(0,4),(0,5),(0,6)]
    #degrees = [7, 2,3,3,3,3,3,1]
    #neighbours = {0:[0,1,2,3,4,5,6,7], 1:[0,1,2],2:[0,1,2,3],3:[0,2,3,4],4:[0,3,4,5],5:[0,4,5,6],6:[0,5,6,7],7:[0,6,7]}
    #clique = [(0,1),(0,3),(0,4),(0,7),(1,2),(2,3),(5,6),(6,7)]
    #neighbours = {0:[0,1,3,4,5],1:[0,1,2],2:[1,2,3],3:[0,2,3],4:[0,4],5:[5,6],6:[5,6,7],7:[0,6,7]}
    clique = [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(3,6),(3,7)]
    neighbours = {0:[0,1],1:[0,1,2], 2:[1,2,3],3:[2,3,4,6,7], 4:[3,4,5], 5:[4,5,6],6:[3,5,6],7:[3,7]}
    degrees = [len(neighbours[i]) - 1 for i in xrange(0, 8)]
    G = nx.Graph()
    G.add_nodes_from(xrange(0, 8))
    G.add_edges_from(clique)
    if len(sys.argv) <= 1:
        CheckTables(CombineRouteIterators(8, neighbours), 8,clique, G,degrees,2)
    else:
        f = open(sys.argv[1])
        for line in f:
            table = eval(line)
            if CheckRoutingTable(table, 8, clique, G, degrees, 1):
                print str.format("{0}", table)
    #for route_table in CombineRouteIterators(5, neighbours):
    #    print route_table
        
