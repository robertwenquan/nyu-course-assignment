#!/usr/bin/python

def shoot2_rough(AA, n, m):
  if (2*m >=n):
    return sum(AA)
  else:
    left_max = sum(AA[0:m])
    right_sum = sum(AA[m:2*m])
    total_max = left_max + right_sum
    tail_buffer = []

    for left_start_idx in range(1,m+1):
      tail_buffer.append(sum(AA[left_start_idx:left_start_idx+m]))

    for right_start_idx in range(m+1,n-m+1):
      left_max = max(left_max, tail_buffer.pop(0))
      right_sum = sum(AA[right_start_idx:right_start_idx+m])
      tail_buffer.append(right_sum)
      total_max = max(total_max, left_max + right_sum)

    return total_max

#Case 1: n = 8, m = 3, scores are [1, 2, 6, 0, 5, 4, 3, 4]
#Answer: 22
#Case 2: n = 6, m = 2, scores are [1, 2, 3, 3, 2, 1]
#Answer: 10
#Case 3: n = 7, m = 1, scores are [1, 7, 2, 9, 3, 4, 5]
#Answer: 16
#Case 4: n = 5, m = 5, scores are [1, 2, 3, 4, 5]
#Answer: 15

def shoot2(AA, n, m):
  if (2*m >=n):
    return sum(AA)

  left_max = sum(AA[0:m])
  right_sum = sum(AA[m:2*m])
  total_max = left_max + right_sum
  tail_buffer = []

  left_sum = left_max
  for left_start_idx in range(1,m+1):
    left_sum = left_sum - AA[left_start_idx-1] + AA[left_start_idx+m-1]
    tail_buffer.append(left_sum)

  for right_start_idx in range(m+1,n-m+1):
    left_popup = tail_buffer.pop(0)
    if (left_popup > left_max):
      left_max = left_popup
    right_sum = right_sum - AA[right_start_idx-1] + AA[right_start_idx+m-1]
    tail_buffer.append(right_sum)
    if (left_max + right_sum > total_max):
      total_max = left_max + right_sum

  return total_max

A = [1, 2, 6, 0, 5, 4, 3, 4]
print shoot2(A, 8, 3)
A = [1, 2, 3, 3, 2, 1]
print shoot2(A, 6, 2)
A = [1, 7, 2, 9, 3, 4, 5]
print shoot2(A, 7, 1)
A = [1, 2, 3, 4, 5]
print shoot2(A, 5, 5)

