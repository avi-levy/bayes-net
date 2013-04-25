from constants import constants
from functools import partial

class factor(object):
        def __init__(self, thing):
                if isinstance(thing, factor): # copy constructor
                        self.vars = list(thing.vars)
                        self.probabilities = dict(thing.probabilities)
                        return
                self.vars = list(thing) # coerce to list
                self.probabilities = {} # maps tuples of {T,F}^|vars| -> values
                return
        def __repr__(self):
#                ret = ""
#                for key, value in self.probabilities.items():
#                        for i in range(len(self.vars)):
#                                ret += "%s=%s, " % (self.vars[i], key[i])
#                        ret += ": %f\n" % value
#                return ret
                return self.probabilities.__repr__()

        # Access operations #
        
        def each(self, operation):
                ''' Applies operation to each semantic, as a dictionary of event-truth pairs, and updates the data structure with the return value '''
                semantic = {}
                def assign(tup):
                        for i in range(len(tup)):
                                semantic[self.vars[i]] = tup[i]
                                return operation(semantic)
                self.fill((), assign)
                
        def fill(self, assigned, operation):
                if len(assigned) == len(self.vars):
                        self.probabilities[assigned] = operation(assigned)
                        return
                for truth in constants.truths:
                        self.fill(assigned + (truth,), operation)

        def lookup(self, semantic):
                tup = ()
                for var in self.vars:
                        tup += (semantic[var],)
                return self.probabilities[tup]
        
        # Algebraic operations #
                
        @staticmethod
        def extend(old, i, value):
                ''' extend a tuple '''
                new = list(old)
                new.insert(i, value)
                return tuple(new)
                
        def sumOut(self, var):
                ''' sum out var from the list of vars '''
                if not var in self.vars:
                        return
                i = self.vars.index(var)
                self.vars.pop(i)
                                
                def update(semantic, truth):
                        a = factor.extend(semantic, i, truth)
                        ret = self.probabilities[a]
                        del self.probabilities[a]
                        return ret

                self.fill((), lambda k: sum(map(partial(update, k), constants.truths)))
                return self
                
        def times(self, other):
                f = factor(set(self.vars) | set(other.vars))
                f.each(lambda semantic: self.truth(semantic) * other.truth(semantic))
                return f
                
        @staticmethod
        def product(factors):
                base = factors.pop()
                if not factors:
                        return base
                return base.times(factor.product(factors))
                
