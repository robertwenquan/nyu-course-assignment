#!/usr/bin/python

AA = [9, 7, 7, 2, 1, 3, 7, 5, 4, 7, 3, 3, 4, 8, 6, 9]

def find_local_minimum(AA, start, end):

  mid = (start + end)/2

  if (AA[mid] > AA[mid-1]):
    return find_local_minimum(AA, start, mid-1)
  elif (AA[mid] > AA[mid+1]):
    return find_local_minimum(AA, mid+1, end)
  else:
    return mid

idx = find_local_minimum(AA, 0, len(AA)-1)
print idx

