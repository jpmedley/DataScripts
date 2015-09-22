#!/usr/bin/python

import os
import string

listing = os.listdir(".")
for file in listing:
  if string.find(file, ".html"):
    print file
