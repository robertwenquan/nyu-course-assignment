#!/usr/bin/python

import timeit

def generate_price(n):
  price_list = dict()

  unit_price = 1

  for i in range(1,n+1):
    price_list[i] = unit_price * i

  return price_list

def generate_price2(n):
  price_list = dict()

  price_list[0] = 0
  price_list[1] = 1
  price_list[2] = 5
  price_list[3] = 8
  price_list[4] = 10
  price_list[5] = 13

  return price_list


# naive recursive way
def rod_cutting0(n, PRICE):

  if n == 0:
    return 0

  result = PRICE[1] + rod_cutting0(n-1, PRICE)

  for i in range(2,n+1):
    current = PRICE[i] + rod_cutting0(n-i, PRICE)
    if (current > result):
      result = current

  return result


# naive recursive way
def rod_cutting1(n, PRICE):

  if n == 0:
    return 0

  pricelist=[]

  for i in range(1,n+1):
    current = PRICE[i] + rod_cutting1(n-i, PRICE)
    pricelist.append(current)

  return max(pricelist)


# top-down memorization method
def memo_rod_cutting(n, PRICE):
  CACHE = dict()
  for i in range(0,n+1):
    CACHE[i] = -1

  return memo_rod_cutting_aux(n, PRICE, CACHE)


# memo way
def memo_rod_cutting_aux(n, PRICE, CACHE):

  if (CACHE[n] != -1):
    return CACHE[n]

  if (n == 0):
    CACHE[n] = 0
    return 0

  result = PRICE[1] + memo_rod_cutting_aux(n-1, PRICE, CACHE)
  for i in range(2,n+1):
    current = PRICE[i] + memo_rod_cutting_aux(n-i, PRICE, CACHE)
    if (current > result):
      result = current

  CACHE[n] = result
  return result


# bottom-up method
def rod_cutting_bottom_up(n, PRICE):
  RESULT = dict()
  RESULT[0] = 0

  for i in range(1,n+1):
    list = []
    for j in range(1,i+1):
      price = PRICE[j] + RESULT[i-j]
      list.append(price)

    RESULT[i] = max(list)

  return RESULT[n]


n = 20
ROD_PRICE = generate_price(n)
print rod_cutting0(n, ROD_PRICE)
print rod_cutting1(n, ROD_PRICE)
print memo_rod_cutting(n, ROD_PRICE)
print rod_cutting_bottom_up(n, ROD_PRICE)

print timeit.timeit(stmt="rod_cutting0(n, ROD_PRICE)", setup="from __main__ import rod_cutting0, n, ROD_PRICE", number=1)
print timeit.timeit(stmt="rod_cutting1(n, ROD_PRICE)", setup="from __main__ import rod_cutting1, n, ROD_PRICE", number=1)
print timeit.timeit(stmt="memo_rod_cutting(n, ROD_PRICE)", setup="from __main__ import memo_rod_cutting, n, ROD_PRICE", number=1)
print timeit.timeit(stmt="rod_cutting_bottom_up(n, ROD_PRICE)", setup="from __main__ import rod_cutting_bottom_up, n, ROD_PRICE", number=1)

