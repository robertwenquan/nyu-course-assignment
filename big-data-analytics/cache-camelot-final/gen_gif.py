#!/usr/bin/python

"""
INPUT: A file named specified from the command line
       The file is a single line JSON format like this:
       ["424344455354X738492939495", "424344535463X738492939495"]
       each element represents a game canvass map

INTERMEDIATE OUTPUT: a series of png files numbered from 0
                     like 0.png, 1.png, 2.png, etc.

OUTPUT: an animated GIF named 'animated.gif'
        with 1 frame per sec and infinite play loop

EXAMPLE: ./gen_gif.py

TODO: 
  1. output file naem through comand line argument
  2. list through command line argument
  3. a switch to save/not-save intermediate results
"""

import os
import sys
import json
from PIL import Image, ImageSequence

FILENAME = sys.argv[1]

with open(FILENAME) as fp:
  for line in fp:
    line = line.strip()
    map_list = json.loads(line)

    n = len(map_list)
    idx = 0

    for mapkey in map_list:
      print 'Generating %d of %d canvass maps...' % (idx+1, n)
      os.system('./draw_canvass.R %s %s.png %d %d &>/dev/null' % (mapkey, idx, n, idx))
      idx += 1

    print 'Generating animated GIF for the %d canvass maps...' % n
    os.system('convert -delay 100 -loop 0 *.png animated.gif')

