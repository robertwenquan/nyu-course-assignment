#!/usr/bin/env python

"""
check lexicons

check the phase1 or phase2 output lexicon files
for debugging purpose

"""

import os
import sys
from struct import unpack, calcsize


def main(filename):
  """ main routine """

  lex_schema = 'iiih'

  if not os.path.exists(filename):
    print 'error'

  offset = 0
  rec_size = calcsize(lex_schema)

  try:
    fd = open(filename)
    while True:
      data = fd.read(rec_size)
      if data == '':
        break

      aa = unpack(lex_schema, data)
      print aa
  except IOError:
    # to handle the piped output to head
    # like cmd | head
    fd.close()

if __name__ == '__main__':
  main(sys.argv[1])

