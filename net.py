from factor import factor
from event import event
import constants
import output

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

        def enum(self, _variables, _evidence):
                variables, evidence = list(_variables), dict(_evidence)

                def next(variables):
                        def noParents(variable):
                                for parent in self.nodes[variable].parents:
                                        if parent in variables:
                                                return False
                                return True
                                
                        orphans = filter(noParents, variables)
                        return variables.pop(variables.index(min(orphans)))                

                def product():
                        ret = self.nodes[variable].probability(evidence)
                        self.trace = variable
                        if variables:
                               multiplier, trace = self.enum(variables, evidence)
                               self.trace = variable + " " + trace
                               ret *= multiplier
                        return ret
                        
                def sumOut(truth):
                        evidence[variable] = truth
                        return product()
                        
                variable = next(variables)
                if variable in evidence.keys():
                        ret = product()
                else:
                        ret = sum(map(sumOut,constants.truths))
                
                output.enum(evidence, self.trace, ret)
                return (ret, self.trace)
                
        def elim(self, query, evidence):
                factors = []
                variables = list(self.nodes.keys())
                known = evidence.keys()
                
                def makeFactor(variable, inputs):
                        def process(semantic):
                                augmented = dict(semantic.items() + evidence.items())
                                return self.nodes[variable].probability(augmented)
                        return factor(inputs, process)
                                
                def next(variables):
                        def noChildren(variable):
                                for another in variables:
                                        if (another is not variable) and (variable in self.nodes[another].parents):
                                                return False
                                return True

                        # make sure none of the remaining variables have us as a parent                                
                        childless = filter(noChildren, variables)
                        
                        def semantics(variable):
                                ''' pre-compute the semantics of the factor table for variable '''
                                semantic = [] if variable in known else [variable]
                                for parent in self.nodes[variable].parents:
                                        if parent not in known:
                                                semantic.append(parent)
                                return semantic

                        # maintain a set of childless vars with minimal factor dimension
                        small = {} # a dictionary mapping minimal factor variables to their semantics
                        for variable in childless:
                                if not small:
                                        semantic = semantics(variable)
                                        small = {variable: semantic}
                                        smallest = len(semantic)
                                else:
                                        semantic = semantics(variable)
                                        size = len(semantic)
                                        if size == smallest:
                                                small[variable] = semantic
                                        if size < smallest:
                                                small = {variable: semantic}
                                                smallest = size

                        # return the alphabetically first small variable
                        variable = min(small, key = small.get)
                        variables.remove(variable)
                        semantic = small[variable]
                        return variable, makeFactor(variable, semantic)
                        
                while variables:
                        variable, _factor = next(variables)
                        factors.append(_factor)
                        if variable is not query and variable not in known:
                                factors = [factor.product(factors).sumOut(variable)]
                        output.elim(variable, factors)
                return factor.product(factors).probabilities
                
        def probability(self, event, evidence, algtype):
                def explore(truth):
                        evidence[event] = truth
                        return (truth,self.enum(self.nodes.keys(), evidence)[0])
                return self.elim(event, evidence) if algtype else dict(map(explore,constants.truths))
