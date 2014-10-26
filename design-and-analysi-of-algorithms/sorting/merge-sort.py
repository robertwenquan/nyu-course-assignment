#!/usr/bin/python

import random

def merge1(AA, start, mid, end):
  pass

def merge2(AA, start, mid, end):

  A1 = AA[start:mid+1]
  B1 = AA[mid+1:end+1]

  index_A1, lens_A1 = 0, len(A1)
  index_B1, lens_B1 = 0, len(B1)

  for AA_idx in range(start, end+1):
    if (index_A1 == lens_A1):
      AA[AA_idx] = B1[index_B1]
      index_B1 += 1
      continue

    if (index_B1 == lens_B1):
      AA[AA_idx] = A1[index_A1]
      index_A1 += 1
      continue

    if (A1[index_A1] < B1[index_B1]):
      AA[AA_idx] = A1[index_A1]
      index_A1 += 1
    else:
      AA[AA_idx] = B1[index_B1]
      index_B1 += 1

def merge_sort(AA, start, end):

  if (start == end):
    return

  mid = int((start + end)/2)

  merge_sort(AA, start, mid)
  merge_sort(AA, mid+1, end)

  merge2(AA, start, mid, end)


RANGE=20
AA = [random.randint(1, RANGE*999) for i in range(1,RANGE)]
print AA
merge_sort(AA, 0, len(AA)-1)
print AA

