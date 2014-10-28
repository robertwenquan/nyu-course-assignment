#!/usr/bin/python

import random

def binary_search(AA, key, start, end):
  mid = int((start+end)/2)

  if (start > end):
    return -1

  if (key == AA[mid]):
    return mid
  elif (key < AA[mid]):
    return binary_search(AA, key, start, mid-1)
  else:
    return binary_search(AA, key, mid+1, end)


RANGE=20
AA = [random.randint(1, RANGE*1) for i in range(1,RANGE)]
print AA
AA = sorted(AA)
print AA

for i in range(1,5):
  search_key = random.randint(1, RANGE*1)
  print "Search key(%d) in %s" % (search_key, AA)
  key = binary_search(AA, search_key, 0, len(AA)-1)
  if (key == -1):
    print "Not Found!!"
  else:
    print "Found at key(%d) at location(%d)" % (search_key, key)
