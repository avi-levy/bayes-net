#!/usr/bin/env python

from sys import argv
from net import *

usage = "usage: bayes <bayesnet> <enum|elim> <query>\n<bayesnet> is the name of the file containing the bayes net.\n<enum|elim> specify the algorithm to use.\n<query> is the probability to compute, specified in quotes."
def end(message=usage):
  print message
  exit(0)

if len(argv) != 4:
  end()
  
filename, infile, alg, query = argv

if not alg in ["enum", "elim"]:
        end("Unknown algorithm; please use enum or elim")
try:
        query = query.split('"')
        if len(query) > 1:
                query = query[1]
        else:
                query = query[0]
        # Do this in two steps to avoid accidentally removing an initial or terminal P inside the parenthesis - since a variable is allowed to be named P
        query = query.strip("P").strip("()")
        # Now query looks like C|A=f,E=t or C
        parts = query.split("|")
        
        var = parts[0]
        assignments = {}
        
        if len(parts) > 1:
                for term in parts[1].split(","):
                        if term:
                                name, value = tuple(term.split("="))
                                assignments[name] = value
except Exception:
        end('Could not parse query string. Make sure it is of this form, INCLUDING quotes: "P(C|A=f,E=t)" or "P(C)"')
        
print "You asked me to compute: %s | %s" % (var, assignments)

bn = net(infile)

print "Start computation."
print bn.compute(var,assignments)
