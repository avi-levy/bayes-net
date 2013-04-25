from constants import constants

class event(object):
        def __init__(self, tableHeading):
                '''
                tableHeading is the heading of the data table for this event
                '''
                self.parents = []
                self.name = None
                self.data = {}                
                if tableHeading.startswith('P('):
                        left, right = tuple(tableHeading.split("="))
                        self.name = left.strip().strip("P").strip("()")
                        self.data[()] = float(right)
                        return
                parents, name = tuple(tableHeading.split('|'))
                self.parents = parents.split()
                self.name = name.strip()

        def setProbabilities(self, row):
                # TODO: add consistency checks against the parents we intialized with
                if row.startswith('-'):
                        return
                bools, value = tuple(row.split("|"))
                self.data[tuple(bools.split())] = float(value)

        def __repr__(self):
                return "\nEvent %s | %s:\n%s" % (self.name, self.parents, self.data)
        
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
