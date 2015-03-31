#!/usr/bin/python

import sys
import json
import string
from pprint import pprint

FILENAME = sys.argv[1]

print "DROP TABLE IF EXISTS flickr_pics;"
print "CREATE TABLE flickr_pics (timestamp time, imgurl varchar(256), blogurl varchar(256), labels varchar(512));"

f = open(FILENAME,'r')

for line in f.readlines():
  item = json.loads(line)

  imgurl = item['url']
  labels = string.replace(','.join(item['labels']), "'", "\\'")
  blogurl = item['tumblr_blogurl']
  timestamp = int(item['tumblr_timestamp'])

  try:
    print "INSERT INTO flickr_pics (timestamp, imgurl, blogurl, labels) VALUES(%d,'%s','%s','%s');" % (timestamp, imgurl, blogurl, labels.encode('utf-8'))
  except:
    continue

