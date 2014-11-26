#!/usr/bin/python

class bcolors:

  TREE = '\033[92m'
  FORWARD = '\033[94m'
  BACK = '\033[91m'
  CROSS = '\033[95m'
  ENDC = '\033[0m'

timestamp = 0

G = { 'q' : { 'adj' : ['s', 't', 'w'] },
      'r' : { 'adj' : ['u', 'y'] },
      's' : { 'adj' : ['v'] },
      't' : { 'adj' : ['x', 'y'] },
      'u' : { 'adj' : ['y'] },
      'v' : { 'adj' : ['w'] },
      'w' : { 'adj' : ['s'] },
      'x' : { 'adj' : ['z'] },
      'y' : { 'adj' : ['q'] },
      'z' : { 'adj' : ['x'] } }
      
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
  node['color'] = 'grey'

  timestamp += 1

  node['time_discov'] = timestamp

  for node_id in node['adj']:
    if G[node_id]['color'] == 'white':
      print bcolors.TREE + node['id'], "->", node_id + " (tree edge)" + bcolors.ENDC
      DFS_VISIT(G[node_id])
    elif G[node_id]['color'] == 'grey':
      print bcolors.BACK + node['id'], "->", node_id + " (back edge)" + bcolors.ENDC
    elif G[node_id]['color'] == 'black':
      if node['time_discov'] < G[node_id]['time_discov']:
        print bcolors.FORWARD + node['id'], "->", node_id + " (forward edge)" + bcolors.ENDC
      else:
        print bcolors.CROSS + node['id'], "->", node_id + " (cross edge)" + bcolors.ENDC

  node['color'] = 'black'

  timestamp += 1
  node['time_finish'] = timestamp


# DFS walk the graph
DFS(G)




print

for node in sorted(G.keys()):
  print str(node) , "[" + str(G[node]['time_discov']) + "," + str(G[node]['time_finish']) + "]"

