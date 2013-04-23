#!/usr/bin/env python

from sys import argv

events = []

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
                return "Event %s:\nParents: %s\nData:\n%s" % (self.name, self.parents, self.data)
        def __str__(self):
                return self.__repr__()
usage = "usage: bayes <bayesnet> <enum|elim> <query>\n<bayesnet> is the name of the file containing the bayes net.\n<enum|elim> specify the algorithm to use.\n<query> is the probability to compute, specified in quotes."
def end(message=usage):
  print message
  exit(0)

if len(argv) != 2:
  end()
  
filename, infile, alg, query = argv

if not alg in ["enum", "elim"]:
        end("Unknown algorithm; please use enum or elim")
try:
        first, last = tuple(query.split('"')[1].split("|"))
        requestedEvent = first.split("(")[1]
        givens = {}
        for term in last.strip(")").split(","):
                name, value = tuple(term.split("="))
                givens[name] = value
except Exception:
        end('Could not parse query string. Make sure it is of this form, INCLUDING quotes: "P(C|A=f,E=t)"')
        
print requestedEvent        
print givens

cur = None
with open(infile) as infile:
  for line in infile:
    line = line.strip()
    if line:
      # print "parsing line %s" % line
      if cur:
        cur.setProbabilities(line)
      else:
        cur = event(line)
    else:
      events.append(cur)
      cur = None
if cur:
        events.append(cur)
for i in events:
  print i

