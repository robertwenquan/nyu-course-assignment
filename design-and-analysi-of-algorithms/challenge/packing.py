#!/usr/bin/python


def smart_packing(packages, limit):

  lens = len(packages)

  # suppose it's merge sort, with ln(n).n complexity
  packages.sort()

  # number of packs to return
  npack = 0

  cnt = 0
  large_index = -1
  small_index = 0

  while True:
    large = packages[large_index]
    small = packages[small_index]

    if (large + small <= limit and cnt+1 <lens):
      large_index -= 1
      small_index += 1
      npack += 1
      cnt += 2
    else:
      large_index -= 1
      npack += 1
      cnt += 1

    if (cnt>=lens):
      break

  return npack

AA = [2]
print smart_packing(AA, 3)

AA = [2, 5, 3, 7]
print smart_packing(AA, 9)

AA =  [1, 2, 3, 4, 5]
print smart_packing(AA, 6)

AA =  [1, 2, 3, 4, 5]
print smart_packing(AA, 100)
