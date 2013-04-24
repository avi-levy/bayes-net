from factor import *

class net(object):
        printTrivial = False # default value is False - don't print empty products; this matches the spec. For debugging purposes, I like to keep it on True.
        truths = ['f','t'] # default truth sort order

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
                
        def factor(self, variable, evidence)
        '''
        Make a factor for the variable, given evidence.
        '''
        
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
                

        def elim(self, query, evidence)
                factors = []
                vars = list(self.entries.keys())
                
                def next(_vars):
                
                
                while vars:
                        var = next(vars)
                        factors.append(net.factor(var, conditions))
                        if var is not query and var not in conditions.keys():
                                factors = [f.product(factors).sumOut(var)]
                        return normalized(f.product(factors))
                
        def compute(self, event, conditions, algtype):
                if algtype is 0:
                        q = {}
                        for truth in net.truths:
                                conditions[event] = truth
                                                        
                                        q[truth] = self.enumerate(self.entries.keys(), conditions)
                else:
                        q = self.elim(event, conditions)
                return net.normalized(q)

        def eliminate(self, _variables, _conditions):
                variables, conditions = list(_variables), dict(_conditions)
                printsofar = "%s | %s =" % (variables, net.formatmy(conditions))
                shouldPrint = net.printTrivial
                if not variables:
                        ret = 1.0
                else:
                        shouldPrint = True                
                        var = self.first(variables) # this means var's parents have been assigned
                        if var in conditions.keys():
                                ret = self.entries[var].lookup(conditions) * self.enumerate(variables, conditions)
                        else:
                                ret = 0.0
                                for truth in net.truths:
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
        def nextForElim(self, variables):# filter out the ancestors first
                # make sure none of the remaining variables have us as a parent
                def noChildren(var):
                        for another in variables:
                                if var in self.entries[var].parents:
                                        return False
                        return True
                        
                candidates = filter(noChildren, variables)
                #print "Orphans left: %s" % orphans
                
                # then pick the first alphabetically
                #print "Best orphan: %s at %d" % (min(orphans),variables.index(min(orphans)))
                
                # TODO: filter out the candidates by factor size as well (so only minimal factor sizes remain)

                return variables.pop(variables.index(min(candidates)))                
                
        def enumerate(self, _variables, _conditions):
                variables, conditions = list(_variables), dict(_conditions)
                printsofar = "%s | %s =" % (variables, net.formatmy(conditions))
                shouldPrint = net.printTrivial
                if not variables:
                        ret = 1.0
                else:
                        shouldPrint = True                
                        var = self.first(variables) # this means var's parents have been assigned
                        if var in conditions.keys():
                                ret = self.entries[var].lookup(conditions) * self.enumerate(variables, conditions)
                        else:
                                ret = 0.0
                                for truth in net.truths:
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
                
class event(object):
        def __init__(self, tableHeading):
                '''
                tableHeading is the heading of the data table for this event
                A B | C
                this means we are event C and we are populating with 4 (A,B) values
                '''
                self.parents = []
                self.name = None
                self.data = {}                
                if tableHeading.startswith('P('):# P(A) = val
                        left, right = tuple(tableHeading.split("="))
                        self.name = left.strip().strip("P").strip("()")
#                        self.name = left.split("(")[1].split(")")[0]
                        self.data = float(right)
                        #print "Created event named %s with data %f and no parents" % (self.name, self.data)
                        return
                parents, name = tuple(tableHeading.split('|')) # there can be a parse error here
                self.parents = parents.split()# important: order is preserved
                self.name = name.strip()
                #print "Create event named %s and parents %s" % (self.name, self.parents)
        def setProbabilities(self, row):
                '''
                ignore row if startswith -
                row is a string. we want to convert it to a dictionary of eventnames to truth values:
                {'A' : True, 'B' : False, ... } and then a value
                
                TODO: add consistency checks against the parents we intialized with
                '''
                if row.startswith('-'):
                        return
                #print "called with %s" % row
                bools, value = tuple(row.split("|"))
                #print "split %s" % bools.split()
                #print "len %d" % len(tuple(bools.split()))
                self.data[tuple(bools.split())] = float(value)
                #print "Data for event %s is now %s" % (self.name, self.data)
        def __repr__(self):
                return "\nEvent %s | %s:\n%s" % (self.name, self.parents, self.data)
        
        def lookup(self, conditions):# assume that our event is already set in the conditions
                if isinstance(self.data, float):
                        if self.name in conditions.keys():
                                return self.data if (conditions[self.name] == 't') else 1 - self.data
                if isinstance(self.data, dict):
                        # iterate through our data entries, until one of them matches the condition
                        # we assume that the conditions permit exactly one valid entry
                        try:
                                for key in self.data:
                                        if self.satisfiesConditions(key, conditions):
                                                return self.data[key] if (conditions[self.name] == 't') else 1 - self.data[key]
                        except Exception:
                                exit("Oh no; the conditions weren't specific enough!")
                exit("Bad bad bad. Make sure the conditions you passed gave us enough info to resolve the probability of this event occurring.")
        def satisfiesConditions(self, key, conditions):
                #print "Checking key %s if satisfies %s" % (key, conditions)
                for i, truth in enumerate(key):
                        if conditions[self.parents[i]] != truth:
                                return False
                return True
        
