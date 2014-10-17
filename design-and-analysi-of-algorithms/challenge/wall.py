#!/usr/bin/python

# if you haven't programmed the program in one shot
# you have logic problem
# and hence need to train your logic
#

def nexti(AA, starti):
  lens = len(AA)

  # last one, just return because there is no further item to search
  if (starti == lens - 1):
    return starti

  val = AA[starti]

  nexti = starti
  for idx in range(starti+1, lens):
    if (AA[idx] == val):
      nexti = idx
    elif (AA[idx] > val):
      break
    else:
      raise(Exception)

  return nexti

def build_bricks(WALL, n):

  # handle special case
  lens = len(WALL)
  if (lens == 1):
    return len(WALL) + n

  # first sort it
  WALL.sort()

  max_idx = lens - 1
  start_idx = nexti(WALL, 0)
  idx = start_idx

  while True:

    if (n == 0):
      break

    WALL[idx] += 1
    n -= 1

    if (idx > 0):
      idx -= 1
      continue
    else: # this is the first one
      idx = nexti(WALL, 1)
      continue

  return WALL[0]

WW = [4, 2, 3, 1, 5, 2]
print build_bricks(WW, 4)

WW = [3, 2, 1]
print build_bricks(WW, 1)

WW = [1]
print build_bricks(WW, 100)

WW = [3, 2, 1]
print build_bricks(WW, 0)

WW = [1, 4, 2, 5, 3, 6]
print build_bricks(WW, 5)
