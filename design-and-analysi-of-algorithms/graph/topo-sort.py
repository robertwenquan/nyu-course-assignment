#!/usr/bin/python

def DFS(graph):

  for node in graph:
    graph[node]['id'] = node
    graph[node]['color'] = 'white'
    graph[node]['time_discov'] = -1
    graph[node]['time_finish'] = -1

  for node in sorted(graph.keys()):
    if graph[node]['color'] == 'white':
      DFS_VISIT(graph[node])

def DFS_VISIT(node):
  
  global timestamp;
  global LIST

  node['color'] = 'grey'

  timestamp += 1

  node['time_discov'] = timestamp

  for node_id in node['adj']:
    if G[node_id]['color'] == 'white':
      DFS_VISIT(G[node_id])

  node['color'] = 'black'

  timestamp += 1
  node['time_finish'] = timestamp

  LIST.insert(0, node['id'])


G = { 'm' : { 'adj' : ['q', 'r', 'x'] },
      'n' : { 'adj' : ['o', 'q', 'u'] },
      'o' : { 'adj' : ['r', 's', 'v'] },
      'p' : { 'adj' : ['o', 's', 'z'] },
      'q' : { 'adj' : ['t'] },
      'r' : { 'adj' : ['u', 'y'] },
      's' : { 'adj' : ['r'] },
      't' : { 'adj' : [] },
      'u' : { 'adj' : ['t'] },
      'v' : { 'adj' : ['w', 'x'] },
      'w' : { 'adj' : ['z'] },
      'x' : { 'adj' : [] },
      'y' : { 'adj' : ['v'] },
      'z' : { 'adj' : [] },
    }
      
timestamp = 0
LIST=[]

# DFS walk the graph
DFS(G)

print "Discovery N Finish Time per vertex: "
for node in sorted(G.keys()):
  print str(node) , "[" + str(G[node]['time_discov']) + "," + str(G[node]['time_finish']) + "]"

print
print "Topology sort order: "
import sys
for i in LIST:
  sys.stdout.write(i + ", ")

print

