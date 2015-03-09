#!/usr/bin/python

import sys

LIST=dict()

for line in sys.stdin:
  line = line.strip()
  node_id,rest = line.split()
  children_list,distance,status,parent_id = rest.split("|")
  distance=int(distance)

  if LIST.get(node_id) == None:
    LIST[node_id] = [node_id,children_list,distance,status,parent_id]
    continue

  if LIST[node_id][1] == "" and children_list != "":
    LIST[node_id][1] = children_list

  if distance >= 0 and distance < LIST[node_id][2]:
    LIST[node_id][2] = distance
    LIST[node_id][4] = parent_id

  if status == "DONE":
    LIST[node_id][3] = "DONE"

  if status == "TODO" and LIST[node_id][3] == "WAIT":
    LIST[node_id][3] = "TODO"

for node_id in LIST:
  node = LIST[node_id]
  print "%s\t%s|%d|%s|%s" % (node[0], node[1], node[2], node[3], node[4])


