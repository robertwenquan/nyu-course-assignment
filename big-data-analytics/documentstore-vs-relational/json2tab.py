#!/usr/bin/python

import sys
import json
from pprint import pprint

FILENAME = sys.argv[1]

f = open(FILENAME,'r')

for line in f.readlines():
  item = json.loads(line)

  imgurl = item['url']
  labels =  ','.join(item['labels'])
  blogurl = item['tumblr_blogurl']
  timestamp = int(item['tumblr_timestamp'])

  try:
    print "%d\t%s\t%s\t%s" % (timestamp, imgurl, blogurl, labels)
  except:
    continue

