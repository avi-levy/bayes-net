def evString(evidence):
        def out(tup):
                return "%s=%s" % tup
        return " ".join(map(out, sorted(evidence.items())))
def enum(evidence, trace, ret):
        ev = evString(evidence)
        print "%s| %s = %1.8f" % (trace.ljust(14), ev.ljust(30), ret)
        
def display(container, event, evidence):
        print "\nRESULT:"
        s = sum(container.values())
        ev = evString(evidence)
        def line(tup):
                truth, value = tup
                truth = truth if not isinstance(truth, tuple) else truth[0] # unbox truth if it is expressed as a tuple (from elim algorithm)
                print "P(%s = %s | %s) = %.16f" % (event, truth, ev, value/s)
        map(line, sorted(container.items()))
