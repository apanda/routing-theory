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
            next_hop = tables[current][inport][dest]
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

def GenerateClique(size):
    clique = []
    for i in xrange(0, size):
        for j in xrange(i + 1, size):
            clique.append((i, j))
    return clique

def CheckRoutingTable(tables, size, clique):
    clique_len = len(clique)
    links = {i : True for i in clique}
    for i in xrange(0, clique_len):
        for j in xrange(i + 1, clique_len):
            for k in xrange(i + 2, clique_len):
                nodes = {x : 0 for x in xrange(0, size)}
                links[clique[i]] = False
                links[clique[j]] = False
                links[clique[k]] = False
                nodes[clique[i][0]] = nodes[clique[i][0]] + 1
                nodes[clique[i][1]] = nodes[clique[i][1]] + 1
                nodes[clique[j][0]] = nodes[clique[j][0]] + 1
                nodes[clique[j][1]] = nodes[clique[j][1]] + 1
                nodes[clique[k][0]] = nodes[clique[k][0]] + 1
                nodes[clique[k][1]] = nodes[clique[k][1]] + 1
                
                max_edges = max(nodes.itervalues())
                if max_edges <= 2:
                    ret = CheckConnectivity(tables, links, size)
                    if not ret:
                        print str.format("""{0} broken by 
    {1}
    {2}
    {3} """, tables, clique[i],clique[j],clique[k])
                        return False
                links[clique[i]] = True
                links[clique[j]] = True
                links[clique[k]] = True
    return True

import sys

if __name__ == "__main__":
    o = open(sys.argv[1])
    clique = GenerateClique(4)
    for line in o:
        r = eval(line)
        if CheckRoutingTable(r, 4, clique):
            print str.format("{0} Can survive", line)
