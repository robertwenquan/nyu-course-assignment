#!/usr/bin/python

class bcolors:

  TREE = '\033[92m'
  FORWARD = '\033[94m'
  BACK = '\033[91m'
  CROSS = '\033[93m'
  ENDC = '\033[0m'

timestamp = 0

G = { 'q' : {
            'id' : 'q',
            'color' : 'white', 
            'time_discov' : -1, 'time_finish' : -1, 
            'adj' : ['s', 't', 'w']
            },
      'r' : {
            'id' : 'r',
            'color' : 'white', 
            'time_discov' : -1, 'time_finish' : -1, 
            'adj' : ['u', 'y']
            },
      's' : {
            'id' : 's',
            'color' : 'white', 
            'time_discov' : -1, 'time_finish' : -1, 
            'adj' : ['v']
            },
      't' : {
            'id' : 't',
            'color' : 'white', 
            'time_discov' : -1, 'time_finish' : -1, 
            'adj' : ['x', 'y']
            },
      'u' : {
            'id' : 'u',
            'color' : 'white', 
            'time_discov' : -1, 'time_finish' : -1, 
            'adj' : ['y']
            },
      'v' : {
            'id' : 'v',
            'color' : 'white', 
            'time_discov' : -1, 'time_finish' : -1, 
            'adj' : ['w']
            },
      'w' : {
            'id' : 'w',
            'color' : 'white', 
            'time_discov' : -1, 'time_finish' : -1, 
            'adj' : ['s']
            },
      'x' : {
            'id' : 'x',
            'color' : 'white', 
            'time_discov' : -1, 'time_finish' : -1, 
            'adj' : ['z']
            },
      'y' : {
            'id' : 'y',
            'color' : 'white', 
            'time_discov' : -1, 'time_finish' : -1, 
            'adj' : ['q']
            },
      'z' : {
            'id' : 'z',
            'color' : 'white', 
            'time_discov' : -1, 'time_finish' : -1, 
            'adj' : ['x']
            },
    }
      
      
def DFS(graph):

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

