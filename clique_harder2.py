#!/usr/bin/env pypy
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
        while True:
            next_hop = tables[current][inport]
            edge = (min(current, next_hop), max(current, next_hop))
            #print str.format("Attempting edge {0}", edge)
            if edge[0] == edge[1] or links[edge]:
                if next_hop == dest:
                    break
                if next_hop in visited:
                    #print "Failing since previsited"
                    return False
                visited_links = []
                visited.append(next_hop)
                inport = current
                current = next_hop
            else:
                if edge in visited_links:
                    return False
                #print "Failing since edge is reused"
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

def CheckRoutingTable(table, size, clique, degrees, k):
    clique_len = len(clique)
    links = {i : True for i in clique}
    import itertools
    remove = itertools.combinations(xrange(0, clique_len), k)
    removed_degree = [0 for x in xrange(0, size)]
    for rem_links in remove:
        for rem_link in rem_links:
            links[clique[rem_link]] = False
            removed_degree[clique[rem_link][0]] = removed_degree[clique[rem_link][0]] + 1
            removed_degree[clique[rem_link][1]] = removed_degree[clique[rem_link][1]] + 1
        if not any(map(lambda x, y: x >= y, removed_degree, degrees)):
            if not CheckConnectivity(table, links, size):
                return False
        for rem_link in rem_links:
            removed_degree[clique[rem_link][0]] = removed_degree[clique[rem_link][0]] - 1
            removed_degree[clique[rem_link][1]] = removed_degree[clique[rem_link][1]] - 1
            links[clique[rem_link]] = True
    return True

import sys
def CheckTables(tables, size, clique, degrees, k):
    count = 0L
    for table in tables:
        count = count + 1
        if count % 1000000 == 0:
            print >>sys.stderr, str.format("Explored {0}", count)
        if CheckRoutingTable(table, size, clique, degrees, k):
            print  str.format("{0}", table)

if __name__ == "__main__":
    clique = [(0,1),(0,2),(0,3),(0,4),(0,5),(1,2),(2,3),(3,4),(4,5)]
    degrees = [5, 2, 3, 3, 3, 2]
    neighbours = {0:[0,1,2,3,4,5], 1:[0,1,2],2:[0,1,2,3],3:[0,2,3,4],4:[0,3,4,5],5:[0,4,5]}
    if len(sys.argv) <= 1:
        CheckTables(CombineRouteIterators(6, neighbours), 6,clique,degrees,2)
    else:
        f = open(sys.argv[1])
        for line in f:
            table = eval(line)
            if CheckRoutingTable(table, 5, clique, degrees, 1):
                print str.format("{0}", table)
    #for route_table in CombineRouteIterators(5, neighbours):
    #    print route_table
        
