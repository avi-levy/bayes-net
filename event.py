from constants import constants

class event(object):
        def __init__(self, line):
                ''' Construct an event from its table heading '''
                if line.startswith('P('):
                        left, right = tuple(line.split("="))
                        self.name = left.strip().strip("P").strip("()")
                        self.parents = []                        
                        self.data[()] = float(right)
                        return
                parents, name = tuple(line.split('|'))
                self.name = name.strip()
                self.parents = parents.split()                
                self.data = {}               
        def __repr__(self):
                return "\nEvent %s | %s:\n%s" % (self.name, self.parents, self.data)                

        def read(self, line):
                ''' Read a line from our conditional probability table '''
                # TODO: add consistency checks against the parents we intialized with
                if line.startswith('-'):
                        return
                bools, value = tuple(line.split("|"))
                self.data[tuple(bools.split())] = float(value)
        
        def probability(self, evidence):
                ''' Return the probability that the evidence is satisfed. '''
                
                def satisfies(semantic):
                        for i, truth in enumerate(semantic):
                                if evidence[self.parents[i]] != truth:
                                        return False
                        return True
                
                for semantic, probability in self.data.items():
                        if satisfies(semantic):
                                return probability if constants.true(evidence[self.name]) else 1 - probability
