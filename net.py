from factor import factor
from constants import constants
from event import event

class net(object):
        '''
        A Bayes net is a set of nodes and node parent data.
        The nodes form a polytree.
        Each node is an event object, see event.py.
        Basically, we can query each node about its conditional probability table.
        That's pretty much it!
        '''
        def __init__(self, file):
                '''
                Read a file that contains a Bayes net.
                This is stored as a series of conditional probability tables.
                Each table specifies an event, its parent events, and probabilities.
                Each time a new table is encountered, we create a new node.
                Then, we pass all of the table data into the event node.
                It handles the rest.
                '''
                self.nodes = {}
                newEntry = True
                for line in open(file):
                        line = line.strip()
                        if not line: # an empty line signals the end of an entry
                                newEntry = True
                                continue
                        if newEntry:
                                entry = event(line) # start a new entry
                                self.nodes[entry.name] = entry # register the entry
                                newEntry = False # reset flag
                        else:
                                entry.read(line) # add to the existing entry
                                
        def __repr__(self):
                return "Net over %s:\n%s" % (self.nodes.keys(), self.nodes)
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
                for parent in self.nodes[variable].parents:
                        if parent not in known:
                                inputs.append(parent)

                def process(semantic):
                        augmented = dict(semantic.items() + evidence.items())
                        return self.nodes[variable].probability(augmented)

                ret = factor(inputs)                        
                ret.each(process)
                return ret

        def elim(self, query, evidence):
                factors = []
                variables = list(self.nodes.keys())
                known = evidence.keys()
                
                def makeFactor(variable, inputs):
                        def process(semantic):
                                augmented = dict(semantic.items() + evidence.items())
                                return self.nodes[variable].probability(augmented)

                        ret = factor(inputs)
                        ret.each(process)
                        return ret
                                
                def next(variables):
                        def noChildren(variable):
                                for another in variables:
                                        if (another is not variable) and (variable in self.nodes[another].parents):
                                                return False
                                return True

                        # make sure none of the remaining variables have us as a parent                                
                        childless = filter(noChildren, variables)
                        
                        # TODO: rename dim to something more descriptive
                        def dim(variable):
                                inputs = [] if variable in known else [variable]
                                for parent in self.nodes[variable].parents:
                                        if parent not in known:
                                                inputs.append(parent)
                                return inputs

                        # maintain a set of childless vars with minimal factor dimension
                        small = {}
                        for variable in childless:
                                if not small:
                                        inputs = dim(variable)
                                        small = {variable: inputs}
                                        smallest = len(inputs)
                                else:
                                        inputs = dim(variable)
                                        size = len(inputs)
                                        if size == smallest:
                                                small[variable] = inputs
                                        if size < smallest:
                                                small = {variable: inputs}
                                                smallest = size

                        # return the alphabetically first small variable
                        variable = min(small, key = small.get)
                        variables.remove(variable)
                        inputs = small[variable]
                        return variable, makeFactor(variable, inputs) # and here was the most recent bug: used var instead of variable...
                        
                while variables:
                        variable, _factor = next(variables)
                        factors.append(_factor)
                        if variable is not query and variable not in known:
                                factors = [factor.product(factors).sumOut(variable)]
                return factor.product(factors).probabilities
                
        def probability(self, event, evidence, algtype):
                if algtype is 0:
                        q = {}
                        for truth in constants.truths:
                                evidence[event] = truth
                                q[truth] = self.enum(self.nodes.keys(), evidence)
                else:
                        q = self.elim(event, evidence)
                return net.normalized(q)

        def enum(self, _variables, _evidence):
                variables, evidence = list(_variables), dict(_evidence)
                printsofar = "%s | %s =" % (variables, net.formatmy(evidence))
                
                def next(variables):
                        def noParents(variable):
                                for parent in self.nodes[variable].parents:
                                        if parent in variables:
                                                return False
                                return True
                                
                        orphans = filter(noParents, variables)
                        return variables.pop(variables.index(min(orphans)))                

               
                def product():
                        ret = self.nodes[var].probability(evidence)
                        if variables:
                               ret *= self.enum(variables, evidence)
                        return ret
                        
                def sumOut(truth):
                        evidence[variable] = truth
                        return product()
                        
                variable = next(variables) # this means var's parents have been assigned
                if variable in evidence.keys():
                        ret = product()
                else:
#                        ret = 0.0
                        ret = sum(map(sumOut,constants.truths))
#                        for truth in constants.truths:
#                                evidence[var] = truth
#                                cur = self.nodes[var].probability(evidence)
#                                if variables:
#                                        cur *= self.enum(variables, evidence)
#                                ret += cur
                print "%s %s" % (printsofar, ret)
                return ret
