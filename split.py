#!/usr/bin/python

import os
import sys

print(sys.argv[1])

def newOutFile(name):
    print(name)

if len(sys.argv) != 3:
    raise Exception("Wrong number of arguments.")
if (sys.argv[1] != '-f') and (sys.argv[1] != '--file'):
    raise Exception("Argument " + sys.argv[1] + " not supported.")
if not os.path.isfile(sys.argv[2]):
    raise Exception("File " + sys.argv[2] + " not found.")

with open(sys.argv[2]) as data:
    for line in data:
        if line.find('Estimated') == 0:
            outFile = newOutFile(line.rpartition(' ')[2])
            
