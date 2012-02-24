#!/usr/bin/env python
def CheckConnectivity(tables, links):
    #for origin in xrange(0, 4):
    #    for dest in xrange(origin + 1, 4):
    dest = 0
    for origin in xrange(1, 4):
        #print str.format("Routing between {0} and {1}", origin, dest)
        visited = []
        visited_links = []
        current = origin
        inport = origin
        while True:
            next_hop = tables[current][inport][dest]
            edge = (min(current, next_hop), max(current, next_hop))
            #print str.format("Attempting edge {0}", edge)
            if edge in links or edge[0] == edge[1]:
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

def GenerateClique(size):
    clique = []
    for i in xrange(0, size):
        for j in xrange(i + 1, size):
            clique.append((i, j))
    return clique

def CheckRoutingTable(tables, size):
    clique = GenerateClique(size)
    for i in xrange(0, len(clique)):
        for j in xrange(i + 1, len(clique)):
            links = []
            #print str.format("Removing links {0} and {1}", clique[i], clique[j])
            for k in xrange(0, len(clique)):
                if k != i and k != j:
                    links.append(clique[k])
            
            ret = CheckConnectivity(tables, links)
            
            if not ret:
                return False
    return True

def RoutesIterator(size):
    route = [[0] for x in xrange(0, size)]
    carry = 0
    while carry == 0:
        yield route
        carry = 1
        i = 0
        while carry == 1 and i < size:
            carry = (route[i][0] + carry) / size
            route[i][0] = (route[i][0] + 1) % size
            i = i+1

def CombineIterators(size):
    routes = []
    for x in RoutesIterator(size):
        routes.append(map(lambda y: list(y), x))
    carry = 0
    route = [0 for x in xrange(0, size)]
    routes_size = len(routes)
    while carry == 0:
        yield [routes[i] for i in route]
        carry = 1
        i = 0
        while carry == 1 and i < routes_size:
            carry = (route[i] + carry) / routes_size
            route[i] = (route[i] + 1) % routes_size
            i = i + 1

def Exhaustive(size):
    total = 0L
    for routes in CombineIterators(size):
        total = total + 1
        #print "Checking new table"
        ret = CheckRoutingTable(routes, size)
        #print routes
        if ret:
            print str.format("Found good routing table {0}",routes)
    print str.format("Explored {0} total", total)
    return True

if __name__ == "__main__":
    if not Exhaustive(4):
        print "No path"
