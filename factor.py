import random
from constants import constants

class factor(object):
        def __init__(self, thing):
                if isinstance(thing, factor): # copy constructor
                        self.vars = list(thing.vars)
                        self.data = dict(thing.data)
                        return
                self.vars = list(thing) # coerce to list
                self.data = {} # maps tuples of {T,F}^|vars| -> values
                self.fill((),self.assign)
                random.seed()
                return

                
        def assign(self, assignment):
                self.data[assignment] = random.random()

        def fill(self, assigned, operation):
                if len(assigned) == len(self.vars):
                        operation(assigned) # put computation here
                        return
                for truth in constants.truths:
                        self.fill(assigned + (truth,), operation)
                        
        def sumOut(self, var): # mutate the data structure
                if not var in self.vars:
                        return
                # fullData = dict(self.data)

                i = self.vars.index(var)
                self.vars.pop(i)
                                
                def sumAssign(assignment):
                        s = 0.0
                        for truth in constants.truths:
                                a = list(assignment)
                                #print "%s %s" % (a, isinstance(a,list))
                                a.insert(i, truth)
                                #print "success"
                                a = tuple(a)
                                s += self.data[a]
                                del self.data[a]
                        self.data[assignment] = s

                self.fill((), sumAssign)                        
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
        @staticmethod
        def product(factors): # if factors is empty we error
                base = factors.pop()
                #print base
                #print factors
                if not factors:
                        return base
                return base.times(factor.product(factors))
                
