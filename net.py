class inference(object):
        def __init__(self, net):
                self.net = net
class net(object):
        def __init__(self, file):
                self.entries = []
                self.vars = set()
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
                        self.entries.append(entry)                

        def add(self, entry):
                self.entries.append(entry)
                self.vars.add(entry.name)
        def __repr__(self):
                return "Net over %s:\n%s" % (self.vars, self.entries)
                
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
                        self.name = left.split("(")[1].split(")")[0]
                        self.data = float(right)
                        #print "Created event named %s with data %f and no parents" % (self.name, self.data)
                        return
                parents, name = tuple(tableHeading.split('|')) # there can be a parse error here
                self.parents = parents.split()# important: order is preserved
                self.name = name
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
