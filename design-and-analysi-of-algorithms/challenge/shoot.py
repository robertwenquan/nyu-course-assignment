#!/usr/bin/python

def shoot_m_in_n(AA, n, m):
  for start_index in range(0,n-m+1):
    yield sum(AA[start_index:start_index+m])

def max_shoot(XB, n, m):
  return max(shoot_m_in_n(XB, n, m)) 


def max_shoot1(AA, n, m):
  if (m>n):
    raise NameError('Invalid m!')
  elif (m==n):
    return sum(AA)
  else:
    xmax = sum(AA[0:m])
    for start_index in range(1,n-m+1):
      xmax = max(xmax, xmax - AA[start_index-1] + AA[start_index - 1 + m])
    return xmax

AA = [1, 2, 6, 0, 5, 4, 3, 4]
print max_shoot(AA, 8, 3),max_shoot1(AA, 8, 3)

A1=[1,2,3,3,2,1]
print max_shoot(A1,6,2),max_shoot1(A1, 6, 2)
 
A2=[1,2,6,0,5,4,3,4]
print max_shoot(A2,8,3), max_shoot1(A2, 8, 3)
  
A3=[1,2,3,4,5]
print max_shoot(A3,5,5), max_shoot1(A3, 5, 5)

