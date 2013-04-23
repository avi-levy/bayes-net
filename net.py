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
                
        def compute(self, event, conditions):
                q = {}
                for truth in net.truths:
                        conditions[event] = truth
                        q[truth] = self.brute(self.entries.keys(), conditions)
                return net.normalized(q)

        def brute(self, variables, conditions):
                ret = (list(variables), dict(conditions))
                shouldPrint = net.printTrivial
                if not variables:
                        ret += (1.0,)
                else:
                        var = self.first(variables) # this means var's parents have been assigned
                        if var in conditions.keys():
                                ret += (self.entries[var].lookup(conditions) * self.brute(variables, conditions),)
                        else:
                                shouldPrint = True
                                s = 0.0
                                for truth in net.truths:
                                        conditions[var] = truth
                                        #print "=========="
                                        #print self.entries
                                        #print var
                                        s += self.entries[var].lookup(conditions) * self.brute(variables, conditions)
                                ret += (s,)
                
                if shouldPrint:
                        print "%s | %s = %s" % ret
                return ret[2]
                        
        def first(self, variables):
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
                                return self.data if conditions[self.name] else 1 - self.data
                if isinstance(self.data, dict):
                        # iterate through our data entries, until one of them matches the condition
                        # we assume that the conditions permit exactly one valid entry
                        try:
                                for key in self.data:
                                        if self.satisfiesConditions(key, conditions):
                                                return self.data[key] if conditions[self.name] else 1 - self.data[key]
                        except Exception:
                                exit("Oh no; the conditions weren't specific enough!")
                exit("Bad bad bad. Make sure the conditions you passed gave us enough info to resolve the probability of this event occurring.")
        def satisfiesConditions(self, key, conditions):
                #print "Checking key %s if satisfies %s" % (key, conditions)
                for i, truth in enumerate(key):
                        if conditions[self.parents[i]] != truth:
                                return False
                return True
        
