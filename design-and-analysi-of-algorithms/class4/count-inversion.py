#!/usr/bin/python

AA = [-1, 2, 4, 1, 7, 3]
AA = [-1, 5, 6, 2, 3]
AA = [-1, 5, 6, 2, 3, 3, 4, 5, 6, 3, 2, 1, 1]

def count_inversion1(AA):
  lens = len(AA) - 1
  cnt = 0

  for i in range(1, lens+1):
    for j in range(i+1, lens+1):
      if (i<j and AA[i]>AA[j]):
        print i,j, AA[i], AA[j]
        cnt += 1

  print "Total inversions: " , cnt

def count_inversion2(AA, low, high):
  mid = (high + low) / 2
  inv_count = 0

  if (low >= high):
    return 0

  inv_count += count_inversion2(AA, low, mid)
  inv_count += count_inversion2(AA, mid+1, high)

  inv_count += count_inversion2_merge(AA, low, mid, high)
  return inv_count

def count_inversion2_merge(A, low, mid, high):
  B1 = A[low:mid+1]
  B2 = A[mid+1:high+1]

  inv_cnt = 0

  lens_b1 = len(B1)
  lens_b2 = len(B2)
  index_b1 = 0
  index_b2 = 0

  for idx in range(low, high+1):
    if (index_b1 >= lens_b1):
      A[idx] = B2[index_b2]
      index_b2 += 1
    elif (index_b2 >= lens_b2):
      A[idx] = B1[index_b1]
      index_b1 += 1
    elif (B1[index_b1] > B2[index_b2]):
      A[idx] = B2[index_b2]
      index_b2 += 1
      inv_cnt += (lens_b1 - index_b1)
     # inv_cnt += 1
    else:
      A[idx] = B1[index_b1]
      index_b1 += 1

  return inv_cnt

count_inversion1(AA)
inversion_count = count_inversion2(AA, 1, len(AA)-1)

print "Total inversions: " , inversion_count

