#!/usr/bin/python

import sys
import json
import time
import pprint

for line in sys.stdin:
  line = line.strip()
  jsdata = json.loads(line)
  ts = jsdata['tumblr_timestamp']
  timestr = time.strftime("%Y%m", time.localtime(ts))

  if jsdata['labels'] != []:
    for tag in jsdata['labels']:
      print "%s\t%s\t%s" % (tag, "1", timestr)

