#!/usr/bin/env python

from sys import argv
from net import net
import output

usage = "usage: bayes <bayesnet> <enum|elim> <query>\n<bayesnet> is the name of the file containing the bayes net.\n<enum|elim> specify the algorithm to use.\n<query> is the probability to compute, specified in quotes."

if len(argv) != 4:
  exit(usage)
  
filename, infile, alg, query = argv

try:
        algType = ["enum", "elim"].index(alg)
except ValueError:
        exit("Unknown algorithm; please use enum or elim")
try:
        parts = (
        lambda x: x.strip("P").strip("()"))(# remove the leading P for probability, then the parens
                (lambda x: x[0] if len(x) is 1 else x[1])(# remove the unquoted part
                        (lambda x: x.split('"'))(# allow extra quotes
                                query
                        )
                )
        ).split("|")

        event = parts[0]

        evidence = {}
        if len(parts) > 1: # allow empty conditionals
                for term in parts[1].split(","):
                        if term:
                                name, value = tuple(term.split("="))
                                evidence[name] = value
except Exception:
        exit('Could not parse query string. Make sure it is of this form, INCLUDING quotes: "P(C|A=f,E=t)" or "P(C)"')
        
bayes = net(infile)
original = dict(evidence)
output.display(bayes.probability(event, evidence, algType), event, original)
