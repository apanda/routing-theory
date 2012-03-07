#!/usr/bin/env python
clique = [(0,1),(0,2),(0,3),(1,2),(1,3),(2,3)]
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

def CheckRoutingTable(tables):
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

def RoutesIterator():
    for r0 in xrange(0,4):
        for r1 in xrange(0,4):
            for r2 in xrange(0,4):
                for r3 in xrange(0,4):
                    yield [[r0],[r1],[r2],[r3]]

def Exhaustive():
    total = 0L
    for paths0 in RoutesIterator():
        for paths1 in RoutesIterator():
            for paths2 in RoutesIterator():
                for paths3 in RoutesIterator():
                    total = total + 1
                    if total % 10000000 == 0:
                        print str.format("Explored {0}", total)
                    #print "Checking new table"
                    ret = CheckRoutingTable([paths0, paths1, paths2, paths3])
                    if ret:
                        print str.format("Found good routing table {0}",[paths0, paths1, paths2, paths3])
                        return True
    print str.format("Explored {0} total", total)
    return False

if __name__ == "__main__":
    if not Exhaustive():
        print "No path"

