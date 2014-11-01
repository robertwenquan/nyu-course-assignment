#!/usr/bin/python

def bubble_sort(AA):
  lens = len(AA)

  cnt = 0

  for i in range(0,lens-1):
    for j in range(i+1,lens):
      if (AA[j] < AA[j-1]):
        AA[j], AA[j-1] = AA[j-1], AA[j]
        cnt += 1

  return cnt

def merge(AA, start, mid, end):
  A1 = AA[start:mid+1]
  A2 = AA[mid+1:end+1]

  lens_A1, index_A1 = len(A1), 0
  lens_A2, index_A2 = len(A2), 0

  cnt = 0

  for idx in range(start, end+1):

    leftover_A1 = lens_A1 - index_A1

    if (index_A1 == lens_A1):
      AA[idx] = A2[index_A2]
      index_A2 += 1
      cnt += leftover_A1
      continue

    if (index_A2 == lens_A2):
      AA[idx] = A1[index_A1]
      index_A1 += 1
      continue

    if (A2[index_A2] < A1[index_A1]):
      AA[idx] = A2[index_A2]
      index_A2 += 1

      cnt += leftover_A1
    else:
      AA[idx] = A1[index_A1]
      index_A1 += 1

  return cnt

def merge_sort(AA, start, end):
  mid = int((start+end)/2)

  if (start == end):
    return 0

  cnt = 0
  cnt += merge_sort(AA, start, mid)
  cnt += merge_sort(AA, mid+1, end)

  cnt += merge(AA, start, mid, end)

  return cnt


AA = []

f = open('IntegerArray.txt', 'r')
for line in f:
  num = int(line)
  AA.append(num)

#AA = [3, 6, 4, 2, 1, 5]
print merge_sort(AA, 0, len(AA)-1)

