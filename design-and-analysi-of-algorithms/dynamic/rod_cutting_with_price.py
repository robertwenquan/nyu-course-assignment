#!/usr/bin/python

import timeit
import random


def generate_price(n):
  price_list = dict()

  unit_price = 1

  for i in range(1,n+1):
    price_list[i] = unit_price * i

  return price_list


def generate_cutting_cost(n):
  cutting_cost_list = dict()

  for i in range(1,n+1):
    cutting_cost_list[i] = random.randint(3,8)

  return cutting_cost_list


# top-down memorization method
def memo_rod_cutting(n, PRICE, COST):
  CACHE = dict()
  for i in range(0,n+1):
    CACHE[i] = -1

  return memo_rod_cutting_aux(n, PRICE, COST, CACHE)


# memo way
def memo_rod_cutting_aux(n, PRICE, COST, CACHE):

  if (CACHE[n] != -1):
    return CACHE[n]

  if (n == 0):
    CACHE[n] = 0
    return 0

  result = PRICE[1] + memo_rod_cutting_aux(n-1, PRICE, COST, CACHE) - COST[1]
  for i in range(2,n+1):
    current = PRICE[i] + memo_rod_cutting_aux(n-i, PRICE, COST, CACHE) - COST[i]
    if (current > result):
      result = current

  CACHE[n] = result
  return result


# bottom-up method
def rod_cutting_bottom_up(n, PRICE, COST):
  RESULT = dict()
  RESULT[0] = 0

  for i in range(1,n+1):
    list = []
    for j in range(1,i+1):
      price = PRICE[j] + RESULT[i-j] - COST[j]
      list.append(price)

    RESULT[i] = max(list)

  return RESULT[n]


n = 500
ROD_PRICE = generate_price(n)
CUT_PRICE = generate_cutting_cost(n)

n = 5
ROD_PRICE = {1:10, 2:18, 3:24, 4:28, 5:30}
CUT_PRICE = {1:4, 2:5, 3:6, 4:8, 5:8}

print memo_rod_cutting(n, ROD_PRICE, CUT_PRICE)
print rod_cutting_bottom_up(n, ROD_PRICE, CUT_PRICE)

print timeit.timeit(stmt="memo_rod_cutting(n, ROD_PRICE, CUT_PRICE)", setup="from __main__ import memo_rod_cutting, n, ROD_PRICE, CUT_PRICE", number=1)
print timeit.timeit(stmt="rod_cutting_bottom_up(n, ROD_PRICE, CUT_PRICE)", setup="from __main__ import rod_cutting_bottom_up, n, ROD_PRICE, CUT_PRICE", number=1)

