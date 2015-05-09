#!/usr/bin/python

import os
import sys
import json
from PIL import Image, ImageSequence

FILENAME = 'list'

with open(FILENAME) as fp:
  for line in fp:
    line = line.strip()
    map_list = json.loads(line)

    n = len(map_list)
    idx = 0

    for mapkey in map_list:
      os.system('./draw_canvass.R %s %s.png %d %d' % (mapkey, idx, n, idx))
      idx += 1

    os.system('convert -delay 100 -loop 0 *.png animated.gif')

