#!/usr/bin/env python

"""
check GIT, MIT TABLE

check the GIT and MIT index table entries
for debugging purpose

"""

import os
import sys
from struct import unpack, calcsize


def main(filename):
  """ main routine """

  # the schema of GIT and MIT are both 'iih' (10 bytes)
  schema = 'iih'

  if not os.path.exists(filename):
    print 'error'

  offset = 0
  rec_size = calcsize(schema)

  try:
    fd = open(filename)
    while True:
      data = fd.read(rec_size)
      if data == '':
        break

      aa = unpack(schema, data)
      print aa
  except IOError:
    # to handle the piped output to head
    # like cmd | head
    fd.close()

if __name__ == '__main__':
  main(sys.argv[1])

