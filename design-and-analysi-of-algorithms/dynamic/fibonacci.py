#!/usr/bin/python

#TODO: save the result during the traditional one, using top-down memorization

def fib_stupid(n):
  if n == 1 or n == 2:
    return 1
  else:
    return fib_stupid(n-1) + fib_stupid(n-2)

# 2nd approach, using bottom-up
def fib_bottom_up(n):
  fib = dict()

  for i in range(1,n):
    if i == 1 or i == 2:
      fib[i] = 1
    else:
      fib[i] = fib[i-1] + fib[i-2]
    print fib[i]

  return fib[n-1] + fib[n-2]

print fib_stupid(30)
print fib_bottom_up(100)
