#!/usr/bin/python

import sys
import json
import string
from pprint import pprint

FILENAME = sys.argv[1]

print "db.flickr_pics.drop()"

f = open(FILENAME,'r')

for line in f.readlines():

  try:
    print "db.flickr_pics.insert(%s)" % line.encode('utf-8')
  except:
    continue

