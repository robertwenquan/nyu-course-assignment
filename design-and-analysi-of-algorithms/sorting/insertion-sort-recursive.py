#!/usr/bin/python

import random

def insertion_recursive(AA, n):

  # exit condition
  if (n == 0):
    return

  # divide
  insertion_recursive(AA, n-1)

  # merge
  key = AA[n]
  idx = n-1
  while (idx >=0 and key < AA[idx]):
    AA[idx+1] = AA[idx]
    idx -= 1

  AA[idx+1] = key


RANGE=10
AA = [random.randint(1, RANGE*19) for i in range(1,RANGE)]
print AA
insertion_recursive(AA, len(AA)-1)
print AA

