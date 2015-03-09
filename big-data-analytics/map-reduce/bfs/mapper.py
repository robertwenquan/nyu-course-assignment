#!/usr/bin/python

import sys

for line in sys.stdin:
  line = line.strip()

  node_id,rest = line.split()
  children_list,distance,status,parent_id = rest.split("|")
  distance=int(distance)

  if status == "WAIT" or status == "DONE":
    print line
  else:
    print "%s\t%s|%d|%s|%s" % (node_id, children_list, distance, "DONE", parent_id)

    children_list = children_list.split(",")
    for child in children_list:
      # skip empty ID
      if child == "":
        continue

      print "%s\t%s|%d|%s|%s" % (child, "", distance+1, "TODO", node_id)

