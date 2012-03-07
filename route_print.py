import sys
size = int(sys.argv[1])
f = open(sys.argv[2])
for l in f:
    routes = eval(l)
    for route in routes:
        for i in xrange(0, size):
            if i in route:
                print route[i],
            else:
                print 'X',
        print
    print
    print

