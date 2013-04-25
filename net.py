from factor import *

class net(object):
        @staticmethod
        def normalized(q):# assume q is nonempty
                sum = 0.0
                for k in q:
                        sum += q[k]
                for k in q:
                        q[k] /= sum
                return q

        @staticmethod
        def formatmy(conditions):
                ret = ""
                for key in sorted(conditions.keys()):
                        ret += "%s=%s " % (key, conditions[key])
                return ret
                
        def factor(self, variable, evidence):
                '''
                Make a factor for the variable, given evidence.
                '''
                print "Making factor from %s, evidence is %s" % (variable, evidence)
                known = evidence.keys()

                if variable in known:
                        inputs = []
                else:
                        inputs = [variable]
                for parent in self.entries[variable].parents:
                        if parent not in known:
                                inputs.append(parent)
                ret = factor(inputs)
                for key in ret.data:
                        
                        
                        asDict = {}
                        for i in range(len(key)):
                                asDict[inputs[i]] = key[i]                        
                        # add our key values to the evidence

                        full = dict(asDict.items() + evidence.items())

                        lookup = self.entries[variable].lookup(full)
                        print "Reading key: %s full: %s, so full[%s] = %s, raw lookup = %s" % (asDict, full, variable, full[variable], lookup)
                        ret.data[key] = lookup # if (full[variable] == 't') else 1 - lookup # the result of our lookup
                        # see line 209ish return self.data[key] if (conditions[self.name] == 't') else 1 - self.data[key]
                return ret
        def elim(self, query, evidence):
                factors = []
                vars = list(self.entries.keys())
                known = evidence.keys()
                
                def next(_vars):
                        def noChildren(var):
                                for another in _vars:
                                        if (another is not var) and (var in self.entries[another].parents):
                                                return False
                                return True

                        # make sure none of the remaining variables have us as a parent                                
                        candidates = filter(noChildren, _vars)

                        def factorSize(var):
                                inputs = [var] if var in known else []
                                for parent in self.entries[var].parents:
                                        if parent not in known:
                                                inputs.append(parent)
                                return len(inputs)

                        minFactor = -1
                        for c in candidates:
                                size = factorSize(c)
                                if minFactor < 0 or minFactor > size:
                                        minFactor = size

                        candidates = filter(lambda x: factorSize(x) == minFactor, candidates)

                        # return the first alphabetical
                        return _vars.pop(_vars.index(min(candidates)))                   
                
                
                while vars:
                        var = next(vars)
                        # print "Processing %s, remaining: %s" % (var, vars)
                        factors.append(self.factor(var, evidence))
                        # print "Factors:\n%s" % "\n".join(map(factor.__repr__,factors))
                        if var is not query and var not in known:
                                # print "Noticed that %s is hidden, so sum it out" % var

                                current = factor.product(factors)
                                current.sumOut(var)

                                factors = [current]
                                # print "Factors after summing:\n%s" % "\n".join(map(factor.__repr__,factors))
                return factor.product(factors)                
        def __init__(self, file):
                self.entries = {}
                entry = None
                for line in open(file):
                        line = line.strip()
                        if line:
                                if entry:
                                        entry.setProbabilities(line)
                                else:
                                        entry = event(line)
                        else:
                                self.add(entry)
                                entry = None
                if entry:
                        self.add(entry)                

        def add(self, entry):
                self.entries[entry.name] = entry
        def __repr__(self):
                return "Net over %s:\n%s" % (self.entries.keys(), self.entries)
                
        def compute(self, event, conditions, algtype):
                if algtype is 0:
                        q = {}
                        for truth in constants.truths:
                                conditions[event] = truth
                                q[truth] = self.enumerate(self.entries.keys(), conditions)
                else:
                        q = self.elim(event, conditions).data
                        #print ret.data
                        #print ret.vars
                return net.normalized(q)

        def enumerate(self, _variables, _conditions):
                variables, conditions = list(_variables), dict(_conditions)
                printsofar = "%s | %s =" % (variables, net.formatmy(conditions))
                shouldPrint = constants.printTrivial
                if not variables:
                        ret = 1.0
                else:
                        shouldPrint = True                
                        var = self.first(variables) # this means var's parents have been assigned
                        if var in conditions.keys():
                                ret = self.entries[var].lookup(conditions) * self.enumerate(variables, conditions)
                        else:
                                ret = 0.0
                                for truth in constants.truths:
                                        conditions[var] = truth
                                        #print "=========="
                                        #print self.entries
                                        #print var
                                        lookup = self.entries[var].lookup(conditions)
                                        recurse = self.enumerate(variables, conditions)
                                        print "var is %s=%s and: + %s * %s" % (var, conditions[var], lookup, recurse)
                                        #print "Did lookup of %s | %s and got %f" % (var, conditions, lookup)
                                        ret += ( lookup * recurse )
                
                if shouldPrint:
                        print "%s %s" % (printsofar, ret)
                return ret
                        
        def first(self, variables):# filter out the ancestors first
                # filter out variables that have parents also among these variables
                def isOrphan(var):
                        #print "Getting parents of %s"% var
                        for parent in self.entries[var].parents:
                                #print parent
                                if parent in variables:
                                        return False
                        return True
                        
                orphans = filter(isOrphan, variables)
                #print "Orphans left: %s" % orphans
                
                # then pick the first alphabetically
                #print "Best orphan: %s at %d" % (min(orphans),variables.index(min(orphans)))

                return variables.pop(variables.index(min(orphans)))
                

