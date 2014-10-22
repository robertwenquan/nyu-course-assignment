#!/usr/bin/python

def get_next(AA, BB):

  lensA, lensB = len(AA), len(BB)
  indexA, indexB = 0, 0

  while True:
    if (indexA == lensA and indexB == lensB):
      break
    if (indexA == lensA):
      yield BB[indexB]
      indexB += 1
    elif (indexB == lensB):
      yield AA[indexA]
      indexA += 1
    elif (AA[indexA] <= BB[indexB] and indexA < lensA):
      yield AA[indexA]
      indexA += 1
    elif (BB[indexB] <= AA[indexA] and indexB < lensB):
      yield BB[indexB]
      indexB += 1

def last_merge(ARR, start, mid, end, n):

  AA = []
  A1 = ARR[start:mid+1]
  A2 = ARR[mid+1:end+1]

  cnt = 0

  GET = get_next(A1, A2)

  point = 0
  AA.append(GET.next())

  idx = 0
  last_idx = 0
  dont_get_next = 0

  while True:
    if (cnt == n):
      break

    if (dont_get_next == 0):
      try:
        val = GET.next()
      except StopIteration:
        leftover = n-cnt
        return (AA[0] + leftover/(last_idx+1))

    if (val == AA[0]):
      dont_get_next = 0

      idx += 1
      AA.append(val)
      last_idx = idx
      point = idx
    else: # the new value is bigger, keep it and do not put it in the bucket
      dont_get_next = 1

      AA[point] += 1

      cnt += 1

      if (point == 0):
        point = last_idx
      else:
        point -= 1

  return AA[0]

def just_merge(A, start, mid, end):

  B1 = A[start:mid+1]
  B2 = A[mid+1:end+1]

  idx1 = 0
  len1 = len(B1)
  idx2 = 0
  len2 = len(B2)

  for idx in range(start, end+1):
    if (idx1 == len1 and idx2 < len2):
      A[idx] = B2[idx2]
      idx2+=1
      continue

    if (idx2 == len2 and idx1 < len1):
      A[idx] = B1[idx1]
      idx1 += 1
      continue

    if (B1[idx1] < B2[idx2]):
      A[idx] = B1[idx1]
      idx1 += 1
    else:
      A[idx] = B2[idx2]
      idx2 += 1
  
def build_wall_merge(WALL, start, end, nbricks, level_of_recursion):

  lens = len(WALL)
  level_of_recursion += 1

  # special case, only one brick wide
  if (level_of_recursion == 1 and lens == 1):
    return (lens+nbricks)

  if (start == end):
    return

  mid = (start+end)/2
  build_wall_merge(WALL, start, mid, nbricks, level_of_recursion)
  build_wall_merge(WALL, mid+1, end, nbricks, level_of_recursion)

  if (level_of_recursion == 1):
    return last_merge(WALL, start, mid, end, nbricks)
  else:
    just_merge(WALL, start, mid, end)

def build_wall(WALL, nbricks):
  start_pos, end_pos = 0, len(WALL)-1
  return build_wall_merge(WALL, start_pos, end_pos, nbricks, 0)

WALL=[1]
WALL=[1,2,5,2,3,4]
WALL=[1,4,2,5,3,6]
WALL=[1,3]
print build_wall(WALL, 6)

