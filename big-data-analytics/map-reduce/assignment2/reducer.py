#!/usr/bin/python

from operator import itemgetter
import sys

word2count = {}

for line in sys.stdin:
  line = line.strip()
  tag, count, _ = line.split('\t', 3)

  try:
    count = int(count)
    word2count[tag] = word2count.get(tag, 0) + count
  except ValueError:
    pass

sorted_word2count = sorted(word2count.items(), key = itemgetter(0))

for tag, count in sorted_word2count:
  print '%s\t%s' % (tag, count)

