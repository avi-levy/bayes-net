import random
from net import *

class factor(object):
        def __init__(self, vars):
                self.vars = list(vars)
                self.data = {} # maps tuples of {T,F}^|vars| -> values
                self.fill((),self.assign)
                random.seed()
                
        def assign(self, assignment):
                self.data[assignment] = random.random()

        def fill(self, assigned, operation):
                if len(assigned) == len(self.vars):
                        operation(assigned) # put computation here
                        return
                for truth in net.truths:
                        self.fill(assigned + (truth,), operation)
        def __repr__(self):
                ret = ""
                for key in self.data:
                        for i in range(len(self.vars)):
                                ret += "%s=%s, " % (self.vars[i], key[i])
                        ret += ": %f\n" % self.data[key]
                return ret
                
        def lookup(self, entry): # entry is a dict A=t B=f C=t, we map to tuple basically
                tup = ()
                for var in self.vars:
                        tup += (entry[var],)
                return self.data[tup]
                
        def times(self, other):
                f = factor(set(self.vars) | set(other.vars))
                def tAssign(assignment):
                        asDict = {}
                        for i in range(len(assignment)):
                                asDict[f.vars[i]] = assignment[i]
                        f.data[assignment] = self.lookup(asDict) * other.lookup(asDict)
                f.fill((), tAssign)
                return f
                
