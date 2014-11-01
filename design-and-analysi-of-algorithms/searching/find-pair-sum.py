#!/usr/bin/python

import random

def find_pair_sum(AA, key):
  start_idx = 0
  end_idx = len(AA)-1

  while (start_idx < end_idx):
    sum = AA[start_idx] + AA[end_idx]
    if (sum == key):
      return (AA[start_idx], AA[end_idx])

    if (sum < key):
      start_idx += 1
      continue
    else:
      end_idx -= 1
      continue

  return (-1,-1)

RANGE=20
AA = [random.randint(1, RANGE*2) for i in range(1,RANGE)]
AA = sorted(AA)

SEARCH_SUM = random.randint(1, RANGE*1) + random.randint(1, RANGE*1)
print "Search sum(%d) in %s" % (SEARCH_SUM, AA)
RESULT = find_pair_sum(AA, SEARCH_SUM)
if (RESULT == (-1,-1)):
  print "Not found a pair of sum(%d)" % (SEARCH_SUM)
else:
  print "Found sum(%d, %d) = %d" % (RESULT[0], RESULT[1], SEARCH_SUM)
