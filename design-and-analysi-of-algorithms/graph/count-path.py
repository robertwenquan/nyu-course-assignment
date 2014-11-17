#!/usr/bin/python

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
      
      
def COUNT_PATH(graph, start, end):

  for node in graph:
    graph[node]['id'] = node

  return DFS_VISIT(graph[start], graph[end])


def DFS_VISIT(node, end_node):
  
  cnt = 0
  for node_id in node['adj']:

    if G[node_id]['id'] == end_node['id']:
      cnt = cnt + 1
    else:
      cnt = cnt + DFS_VISIT(G[node_id], end_node)

  return cnt


PATH = { 'start' : 'p', 'end' : 'v' }
print "number of PATH from " + PATH['start'] + " to " + PATH['end'] + " is: " + str(COUNT_PATH(G, PATH['start'], PATH['end']))

for start_idx in G:
  for end_idx in G:
    npath = COUNT_PATH(G, start_idx, end_idx)
    if npath > 2:
      print "number of PATH from " + start_idx + " to " + end_idx + " is: " + str(npath)

