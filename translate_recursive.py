#!/usr/bin/env pypy
from copy import deepcopy
def CheckConnectivity(tables, size):
    #for origin in xrange(0, 4):
    #    for dest in xrange(origin + 1, 4):
    dest = 0
    for origin in xrange(1, size):
        #print str.format("Routing between {0} and {1}", origin, dest)
        to_try = [([], [], [], origin, origin, False)]
        while len(to_try) > 0:
            (visited, for_print, edges, current, inport, from_fail) = to_try.pop()
            should_print = False
            while True:
                visited.append(current)
                for_print.append(current)
                next_hop = tables[current][inport]
                edge = (min(next_hop, current), max(next_hop, current))
                if next_hop in visited or edge in edges or edge[0] == edge[1]:
                    break
                edges.append(edge)
                tempvisited = deepcopy(visited)
                tempfor_print = deepcopy(for_print)
                tempfor_print.append(next_hop)
                to_try.append((tempvisited, tempfor_print, deepcopy(edges), current, next_hop, True))
                if next_hop == dest:
                    for_print.append(next_hop)
                    should_print = True
                    break
                inport = current
                current = next_hop
            if should_print:
                pass
                print ','.join(map(str, for_print))
    return True
if __name__=="__main__":
    import sys
    t = open(sys.argv[1])
    for table in t:
        CheckConnectivity(eval(table), 5)
        print
        print
