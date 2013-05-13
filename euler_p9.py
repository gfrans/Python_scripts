#!/usr/bin/python

from itertools import combinations as combo

# Find pythagorean triplet where terms sum to 1000
def findTriple():
  for triple in combo(xrange(1, 998), 3):
    if sum(triple) == 1000:
      if triple[0]**2 + triple[1]**2 == triple[2]**2: return reduce((lambda x,y: x*y), triple)

print "Pythagorean triplet: ", findTriple()
