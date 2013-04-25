from factor import factor

class net(object):
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

                def process(semantic):
                        augmented = dict(semantic.items() + evidence.items())
                        return self.entries[variable].probability(augmented)

                ret = factor(inputs)                        
                ret.each(process)
                return ret

        def elim(self, query, evidence):
                factors = []
                vars = list(self.entries.keys())
                known = evidence.keys()
                
                def makeFactor(variable, inputs):
                        def process(semantic):
                                augmented = dict(semantic.items() + evidence.items())
                                return self.entries[variable].probability(augmented)

                        ret = factor(inputs)                        
                        ret.each(process)
                        return ret
                                
                def next(variables):
                        def noChildren(var):
                                for another in variables:
                                        if (another is not var) and (var in self.entries[another].parents):
                                                return False
                                return True

                        # make sure none of the remaining variables have us as a parent                                
                        childless = filter(noChildren, variables)

                        # TODO: rename dim to something more descriptive
                        def dim(var):
                                inputs = [var] if var in known else []
                                for parent in self.entries[var].parents:
                                        if parent not in known:
                                                inputs.append(parent)
                                return inputs

                        # maintain a set of childless vars with minimal factor dimension
                        small = {}
                        for var in childless:
                                if not small:
                                        inputs = dim(var)
                                        small = {var: inputs}
                                        smallest = len(inputs)
                                else:
                                        inputs = dim(var)
                                        size = len(inputs)
                                        if size == smallest:
                                                small[var] = inputs
                                        if size < smallest:
                                                small = {var: inputs}
                                                smallest = size

                        # return the alphabetically first small variable
                        variable = min(small, key = small.get)
                        variables.remove(variable)
                        inputs = small[variable]
                        return variable, makeFactor(var, inputs)
                        
                while vars:
                        var, _factor = next(vars)
                        factors.append(_factor)
                        if var is not query and var not in known:
                                factors = [factor.product(factors).sumOut(var)]
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
