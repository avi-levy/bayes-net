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
        first, last = tuple(query.split("|"))
        var = first.split("(")[1]
        givens = {}
        for term in last.strip(")").split(","):
                name, value = tuple(term.split("="))
                givens[name] = value
except Exception:
        end('Could not parse query string. Make sure it is of this form, INCLUDING quotes: "P(C|A=f,E=t)"')
        
bn = net(infile)
print bn
