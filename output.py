from operator import itemgetter

def assign(tup):
        return "%s=%s" % tup
def evString(evidence):
        return " ".join(map(assign, sorted(evidence.items())))
def enum(evidence, trace, ret):
        ev = evString(evidence)
        print "%s| %s = %1.8f" % (trace.ljust(14), ev.ljust(30), ret)

def elim(variable, factors):
        print "----- Variable:   %s -----\nFactors:\n%s\n" % (variable, "\n\n".join(map(str,factors)))

def display(container, event, evidence):
        print "\nRESULT:"
        s = sum(container.values())
        ev = evString(evidence)
        def line(tup):
                truth, value = tup
                truth = truth if not isinstance(truth, tuple) else truth[0] # unbox truth if it is expressed as a tuple (from elim algorithm)
                print "P(%s = %s | %s) = %s" % (event, truth, ev, value/s)
        map(line, sorted(container.items()))
        
def factor(probabilities, variables):
        def entry((key, value)):
                def out((i, variable)):
                        return assign((variable, key[i]))
                return ", ".join(map(out, enumerate(variables))) + ": %s" % value

        return "\n".join(map(entry, sorted(probabilities.items(), key=lambda x: x[0][::-1]))) # sort the values by key from outside in
#        for key, value in self.probabilities.items():
#                print ", ".join(map(out, enumerate(variables))) + ": %f" % value
#                for i in range(len(self.vars)):
#                        ret += "%s=%s, " % (self.vars[i], key[i])
#                ret += ": %f\n" % value
#        return ret
        #                return self.probabilities.__repr__()
