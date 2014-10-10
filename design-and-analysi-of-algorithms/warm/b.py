#!/usr/bin/python

def move_on_bubble_sort(AA, lens):
  switch_count = 0
  for i in range(lens, 1, -1):
    for j in range(0, i-1):
      if (AA[j] > AA[j+1]):
        xb = AA[j]
        AA[j] = AA[j+1]
        AA[j+1] = xb
        switch_count += 1
  return switch_count


def move_on_quick_sort(AA, lens):
  switch_count = 0
  return switch_count


def combine_merge_sort(AA, start, mid, end):
  BB = AA[start:end+1]
  switch_count = move_on_bubble_sort(BB, len(BB))
  index_bb = 0

  for idx in range(start, end+1):
    AA[idx] = BB[index_bb]
    index_bb += 1

  return switch_count


def move_on_merge_sort(AA, start, end):
  switch_count = 0

  if (start == end):
    return switch_count

  mid = (start+end)/2

  switch_count += move_on_merge_sort(AA, start, mid)
  switch_count += move_on_merge_sort(AA, mid+1, end)

  switch_count += combine_merge_sort(AA, start, mid, end)

  return switch_count


AA = [1, 7, 2, 9, 3, 4, 5]
lens = len(AA)
print move_on_bubble_sort(AA, lens)

AA = [1, 7, 2, 9, 3, 4, 5]
AA = [3, 2, 1]
lens = len(AA)
print move_on_merge_sort(AA, 0, lens-1)
print AA

