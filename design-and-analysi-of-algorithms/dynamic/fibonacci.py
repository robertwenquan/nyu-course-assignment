#!/usr/bin/python

import timeit

# naive implementation
def fib_naive(n):
  if n == 1 or n == 2:
    return 1
  else:
    return fib_naive(n-1) + fib_naive(n-2)


# 1st approach, cached way
def fib_cached(n):
  cache = dict()
  for idx in range(0,n+1):
    cache[idx] = -1

  return fib_cached_aux(n, cache)

def fib_cached_aux(n, cache):
  if cache[n] != -1:
    return cache[n]

  if (n == 0):
    cache[0] = 0
    return 0
  elif (n == 1):
    cache[1] = 1
    return 1
  else:
    res = fib_cached_aux(n-1, cache) + fib_cached_aux(n-2, cache)
    cache[n] = res
    return res


# 2nd approach, using bottom-up
def fib_bottom_up(n):
  fib = dict()

  for i in range(0,n):
    if i == 0:
      fib[i] = 0
    elif i == 1:
      fib[i] = 1
    else:
      fib[i] = fib[i-1] + fib[i-2]

  return fib[n-1] + fib[n-2]


print fib_naive(30)
print fib_bottom_up(35)
print fib_cached(35)

print timeit.timeit(stmt="fib_naive(35)", setup="from __main__ import fib_naive", number=1)
print timeit.timeit(stmt="fib_bottom_up(35)", setup="from __main__ import fib_bottom_up", number=1)
print timeit.timeit(stmt="fib_cached(35)", setup="from __main__ import fib_cached", number=1)

