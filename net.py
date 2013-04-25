from factor import factor

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
        def formatmy(evidence):
                ret = ""
                for key in sorted(evidence.keys()):
                        ret += "%s=%s " % (key, evidence[key])
                return ret
                
        def factor(self, variable, evidence):
                ''' Construct a factor '''
                known = evidence.keys()
                if variable in known:
                        inputs = []
                else:
                        inputs = [variable]
                for parent in self.entries[variable].parents:
                        if parent not in known:
                                inputs.append(parent)
                ret = factor(inputs)
                for semantic in ret.data:
                        asDict = {}
                        for i in range(len(key)):
                                asDict[inputs[i]] = semantic[i]                        
                        # add our key values to the evidence

                        full = dict(asDict.items() + evidence.items())

                        probability = self.entries[variable].probability(full)
                        print "Reading key: %s full: %s, so full[%s] = %s, raw lookup = %s" % (asDict, full, variable, full[variable], lookup)
                        ret.data[semantic] = probability
                return ret

        def __init__(self, file):
                self.entries = {}
                entry = None
                for line in open(file):
                        line = line.strip()
                        if line:
                                if entry:
                                        entry.read(line)
                                else:
                                        entry = event(line)
                        else:
                                self.entries[entry.name] = entry
                                entry = None
                if entry:
                        self.add(entry)                

        def __repr__(self):
                return "Net over %s:\n%s" % (self.entries.keys(), self.entries)
                
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
                        childless = filter(noChildren, _vars)

                        def dim(var):
                                inputs = [var] if var in known else []
                                for parent in self.entries[var].parents:
                                        if parent not in known:
                                                inputs.append(parent)
                                return len(inputs)

                        # maintain a set of childless vars with minimal factor dimension
                        for var in childless:
                                if not small:
                                        small = [var]
                                        smallest = dim(var)                                        
                                else:
                                        size = dim(var)
                                        if size == smallest:
                                                small.append(var)
                                        if size < smallest:
                                                small = [var]
                                                smallest = size

                        # return the first alphabetical
                        return _vars.pop(_vars.index(min(smallest)))                   
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
                
        def probability(self, event, evidence, algtype):
                if algtype is 0:
                        q = {}
                        for truth in constants.truths:
                                evidence[event] = truth
                                q[truth] = self.enum(self.entries.keys(), evidence)
                else:
                        q = self.elim(event, evidence).data
                return net.normalized(q)

        def enum(self, _variables, _evidence):
                variables, evidence = list(_variables), dict(_evidence)
                printsofar = "%s | %s =" % (variables, net.formatmy(evidence))
                shouldPrint = constants.printTrivial
                
                def next(variables):
                        def noParents(var):
                                for parent in self.entries[var].parents:
                                        if parent in variables:
                                                return False
                                return True
                                
                        orphans = filter(noParents, variables)
                        return variables.pop(variables.index(min(orphans)))                

                if not variables:
                        ret = 1.0
                else:
                        shouldPrint = True                
                        var = next(variables) # this means var's parents have been assigned
                        if var in evidence.keys():
                                ret = self.entries[var].lookup(evidence) * self.enum(variables, evidence)
                        else:
                                ret = 0.0
                                for truth in constants.truths:
                                        evidence[var] = truth
                                        lookup = self.entries[var].probability(evidence)
                                        recurse = self.enum(variables, evidence)
                                        ret += lookup * recurse
                
                if shouldPrint:
                        print "%s %s" % (printsofar, ret)
                return ret
