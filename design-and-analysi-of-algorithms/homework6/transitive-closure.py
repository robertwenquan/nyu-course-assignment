#!/usr/bin/python

import pprint
from operator import itemgetter, attrgetter

def DFS(graph):

  for node in graph:
    graph[node]['id'] = node
    graph[node]['color'] = 'white'
    graph[node]['time_discov'] = -1
    graph[node]['time_finish'] = -1

  for node in sorted(graph.keys()):
    if graph[node]['color'] == 'white':
      DFS_VISIT(graph[node], node)

  return graph

def SINGLE_NODE_DFS(graph, nodeid):

  for node in graph:
    graph[node]['id'] = node
    graph[node]['color'] = 'white'
    graph[node]['time_discov'] = -1
    graph[node]['time_finish'] = -1

  DFS_VISIT(graph[nodeid], nodeid)

  return graph


def DFS_VISIT(node, rootid):
  
  global TRANSITIVE_CLOSURE
  global timestamp

  node['color'] = 'grey'

  timestamp += 1

  node['time_discov'] = timestamp

  for node_id in node['adj']:
    if G[node_id]['color'] == 'white':
      TRANSITIVE_CLOSURE[rootid][node_id] = 1
      DFS_VISIT(G[node_id], rootid)

  node['color'] = 'black'

  timestamp += 1
  node['time_finish'] = timestamp


def init_data(graph):

  tc = dict()

  for id in graph:
    tc[id] = dict()

    for subid in graph:
      if subid == id:
        tc[id][subid] = 1
      else:
        tc[id][subid] = 0

  return tc


def print_transitive_closure_matrix(graph_matrix):
  for id in graph_matrix:
    aa = [graph_matrix[id][subid] for subid in graph_matrix[id]]
    print aa


G = { 1 : { 'adj' : [2] },
      2 : { 'adj' : [1, 3] },
      3 : { 'adj' : [2, 4] },
      4 : { 'adj' : [] },
    }
      

timestamp = 0
TRANSITIVE_CLOSURE = init_data(G.copy())

# DFS walk the graph
TOPO_GRAPH = DFS(G.copy())
TOPO_LIST = [item[0] for item in sorted(TOPO_GRAPH.items(), key = lambda xxx: (-xxx[1]['time_finish']))]

for id in TOPO_LIST:
  SINGLE_NODE_DFS(G.copy(), id)

print_transitive_closure_matrix(TRANSITIVE_CLOSURE)
