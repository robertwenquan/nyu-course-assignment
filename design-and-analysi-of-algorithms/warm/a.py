#!/usr/bin/python


def minimum_move_on_sort(AA, lens):
  switch_count = 0
  for i in range(lens, 1, -1):
    for j in range(0, i-1):
      if (AA[j] > AA[j+1]):
        xb = AA[j]
        AA[j] = AA[j+1]
        AA[j+1] = xb
        switch_count += 1
  return switch_count

AA = [1, 7, 2, 9, 3, 4, 5]
AA = [1, 3, 2, 4]
AA = [3, 2, 1]
lens = len(AA)
print minimum_move_on_sort(AA, lens)
