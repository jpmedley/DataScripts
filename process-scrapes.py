#!/usr/bin/python

import json
import os
import re
import string
import sys

OUT_PATH = "out/"

def processScrapes(startYear, endYear):
  cities = dict() #key = city name, value = years

  listing = os.listdir(OUT_PATH)
  for file in listing:
    if (string.find(file, ".html") > 0):
      currentFile = open((OUT_PATH + file), 'r')
      file = file.rpartition('.')[0]
      year = file[-4:]
      city = file[:(len(file) - 4)]
      # print ("Reading %s for %s" % (city, year))
      if (city not in cities):
        cities[city] = dict()
      for line in currentFile:
        if (string.find(line, "rate vcrime2 murd2") > 0):
          value = re.search('<font size="2">(.*)</font>', line)
          cities[city][year] = value.group(1).strip()
          break

  murders = open(OUT_PATH + 'murders.csv', 'a')
  for city in cities:
    print ("Creating and saving row for %s" % city)
    row = city + "\t"
    year = int(startYear)
    end = int(endYear)
    while (year < end):
      if (str(year) in cities[city]):
        row = row + cities[city][str(year)] + "\t"
      else:
        row = row + "\t"
      year += 1
    row = row + "\n"
    murders.write(row)
  murders.close()
  print "Completed processing crime data."

processScrapes(sys.argv[1], sys.argv[2])