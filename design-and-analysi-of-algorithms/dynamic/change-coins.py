#!/usr/bin/python

# naive implementation
def min_coins(n, COINS):
  if n in COINS:
    return 1

  xx = []
  for coin in COINS:
    if coin < n:
      num = 1 + min_coins(n - coin, COINS)
      xx.append(num)

  return min(xx)

#print min_coins(N, LISTS)


# DP bottom-up implementation
def min_coins_bottom_up(n, COINS):

  RESULT = dict()

  RESULT[1] = 1

  for i in range(2,n+1):
    list = []

    if i in COINS:
      list.append(1)
    else:
      for coin in COINS:
        if coin < i:
          list.append(1 + RESULT[i-coin])

    RESULT[i] = min(list)

  return RESULT[n]

COIN_LISTS = [1,4,5,10]
N = 8

COIN_LISTS = [1,2,5,10,20,25,50,100]
N = 249

print min_coins_bottom_up(N, COIN_LISTS)


