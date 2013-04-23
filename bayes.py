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
                        self.data[{}] = float(right)
                        print "Created event named %s with data %f and no parents" % (self.name, self.data)
                        return
                parents, name = tuple(tableHeading.split('|')) # there can be a parse error here
                self.parents = parents.split()# important: order is preserved
                self.name = name
                print "Create event named %s and parents %s" % (self.name, self.parents)
        def setProbabilities(self, row):
                '''
                ignore row if startswith -
                row is a string. we want to convert it to a dictionary of eventnames to truth values:
                {'A' : True, 'B' : False, ... } and then a value
                
                TODO: add consistency checks against the parents we intialized with
                '''
                if row.startswith('-'):
                        return

                bools, value = tuple(row.split())
                self.data[bools.split()] = float(value)
                print "Data for event %s is now %s" % (self.name, self.data)
        
usage = "usage: bayes write usage string"
def end(message=usage):
  print message
  exit(0)

if len(argv) != 2:
  end()
  
filename, infile = argv

cur = None
with open(infile) as infile:
  for line in infile:
    if line:
      if cur:
        cur.setProbabilities(line)
      else:
        cur = event(line)
    else:
      events.append(cur)
      cur = None
      
