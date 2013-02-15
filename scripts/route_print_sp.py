import sys
size = int(sys.argv[1])
f = open(sys.argv[2])
nodes = ['d','11','3','1','2','10','4','5']
for l in f:
    routes = eval(l)
    print ' ',
    for n in nodes:
        print n,
    print
    for route in routes:
        for i in xrange(0, size):
            if i in route:
                print route[i],
            else:
                print 'X',
        print
    print
    print

