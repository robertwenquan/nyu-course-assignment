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
      
def BFS(graph, start_node_idx):

  for node in graph:
    graph[node]['id'] = node
    graph[node]['color'] = 'white'
    graph[node]['distance'] = 'inf'
    graph[node]['parent'] = 'na'

  process_queue = [start_node_idx]
  graph[start_node_idx]['distance'] = 0

  while process_queue != []:
    idx = process_queue.pop(0)
    node = graph[idx]
    node['color'] = 'black'

    for subnode_id in node['adj']:
      subnode = graph[subnode_id]
      parent_node = graph[idx]

      if subnode['color'] == 'white':
        subnode['color'] = "grey"
        subnode['parent'] = idx
        subnode['distance'] = parent_node['distance'] + 1
        process_queue.append(subnode_id)

  print "Distance: "
  for node in sorted(graph.keys()):
    print str(start_node_idx) + "->" + str(node) , str(graph[node]['distance'])


BFS(G, 'q')

