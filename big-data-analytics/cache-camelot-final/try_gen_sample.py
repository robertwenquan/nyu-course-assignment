#!/usr/bin/python

"""
generate "all" possible game canvass maps

Becanse the magnitude of all canvass maps are huge, 
we use some filtering technique to eliminate some cases like: 
  1. already won case
  2. aggressively defensive mode

Preferrable scenarios are:
  1. close together battling
"""

import itertools

def is_valid_cell(cell_loc):
  """
  check whether a (x,y) coordinate is a valid cell on the game canvass
  """
  if cell_loc not in [ (0,0),  (0,1),  (0,2),  (0,5),  (0,6),  (0,7), \
                       (1,0),  (1,1),                  (1,6),  (1,7), \
                       (2,0),                                  (2,7), \
                      (11,0),                                 (11,7), \
                      (12,0), (12,1),                 (12,6), (12,7), \
                      (13,0), (13,1), (13,2), (13,5), (13,6), (13,7)]:
    return True
  else:
    return False

def gen_valid_cell(side, exclude_list=[]):
  """
  a function that generates valid cell on the game canvass
  
  the invalid/disabled cells are excluded from the list
  """
  for x in range(14):

    if side == 'north' and (x < 4 or x > 12):
      continue
    elif side == 'south' and (x > 9 or x < 1):
      continue

    for y in range(8):
      if (x,y) not in exclude_list and is_valid_cell((x,y)) == True:
        yield (x,y)

def encode_canvass_map(piece_list):
  """
  encode the canvass map into a string

  <north piece list>X<south piece list>
  """
  ret = ''
  for cell in piece_list:
    if cell == (-1, -1):
      ret += 'X'
    else:
      x,y = cell
      ret += hex(x)[2] + hex(y)[2]

  return ret

def gen_canvass_maps():
  """
  geneate all canvass map combinations

  Considerations: 
    1. only consider player with 2-6 pieces
    2. won cases are eliminated
  """
  for n_north in range(6, 1, -1):
    for north_piece_list in itertools.combinations(gen_valid_cell('north'), n_north):
      for n_south in range(6, 1, -1):
        for south_piece_list in itertools.combinations(gen_valid_cell('south'), n_south):
          yield encode_canvass_map(list(north_piece_list) + [(-1,-1)] + list(south_piece_list))

n = 0
for canvass in gen_canvass_maps():
  n += 1
  if n % 1000000 == 0:
    print n
  #print canvass

print n
