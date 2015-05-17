#!/usr/bin/python
#
# learning.py
#
# learn the (x,y) mean of the pieces for north and south each
#
# INPUT: a canvass map hashkey
# OUTPUT: A tuple of two (x,y) tuples

import os


def key_to_canvass(mapkey):
  '''
  hashkey representation of canvass to
  data structure in the game canvass

  INPUT: "404142434445X121314152132"
  OUTPUT: [[(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5)], \
           [(1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (3, 2)]]
  '''

  def unmap_loc(key):
    '''
    string to tuple representation of cell location

    INPUT1: '40'
    OUTPUT1: (4, 0)

    INPUT2: 'a3'
    OUTPUT2: (10, 3)
    '''
    off_x = int(key[0], 16)
    off_y = int(key[1], 16)
    return (off_x, off_y)

  north_pieces = []
  south_pieces = []

  for north_idx in range(0,6):
    north_piece = mapkey[north_idx * 2 : north_idx * 2 + 2]
    north_piece_loc = unmap_loc(north_piece)

    if north_piece_loc != (0, 0):
      north_pieces.append(north_piece_loc)

  for south_idx in range(0,6):
    south_piece = mapkey[13 + south_idx * 2 : 13 + south_idx * 2 + 2]
    south_piece_loc = unmap_loc(south_piece)

    if south_piece_loc != (0, 0):
      south_pieces.append(south_piece_loc)

  return [north_pieces, south_pieces]


def get_loc_mean(loc_list):

  nn = float(len(loc_list))
  sum_x = 0
  sum_y = 0

  for loc in loc_list:
    (off_x, off_y) = loc
    sum_x += off_x
    sum_y += off_y

  return (sum_x/nn, sum_y/nn)

#
# main starts here
#

FILENAME='train/data'

NORTH_RANGE_X = []
NORTH_RANGE_Y = []
SOUTH_RANGE_X = []
SOUTH_RANGE_Y = []

with open(FILENAME) as fp:
  for line in fp:
    line = line.strip()
    north_piece_list, south_piece_list = key_to_canvass(line)

    x, y = get_loc_mean(north_piece_list)
    NORTH_RANGE_X.append(x)
    NORTH_RANGE_Y.append(y)

    x, y = get_loc_mean(south_piece_list)
    SOUTH_RANGE_X.append(x)
    SOUTH_RANGE_Y.append(y)

SORTED_NORTH_RANGE_X = sorted(NORTH_RANGE_X)
SORTED_NORTH_RANGE_Y = sorted(NORTH_RANGE_Y)
SORTED_SOUTH_RANGE_X = sorted(SOUTH_RANGE_X)
SORTED_SOUTH_RANGE_Y = sorted(SOUTH_RANGE_Y)

print 'NORTH RANGE X: (%.2f, %.2f)' % (SORTED_NORTH_RANGE_X[0], SORTED_NORTH_RANGE_X[-1])
print 'NORTH RANGE Y: (%.2f, %.2f)' % (SORTED_NORTH_RANGE_Y[0], SORTED_NORTH_RANGE_Y[-1])
print 'SOUTH RANGE X: (%.2f, %.2f)' % (SORTED_SOUTH_RANGE_X[0], SORTED_SOUTH_RANGE_X[-1])
print 'SOUTH RANGE Y: (%.2f, %.2f)' % (SORTED_SOUTH_RANGE_Y[0], SORTED_SOUTH_RANGE_Y[-1])

