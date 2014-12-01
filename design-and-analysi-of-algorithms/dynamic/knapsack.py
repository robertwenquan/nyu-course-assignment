#!/usr/bin/python



def max_value(SACK, MAX_W):

  value_list = [0]
  for id in SACK:
    (weight, val) = SACK[id]
    
    if weight <= MAX_W:
      NEW_SACK = SACK.copy()
      del NEW_SACK[id]
      value = val + max_value(NEW_SACK, MAX_W - weight)
      value_list.append(value)

  return max(value_list)


def max_value_bottom_up(SACK, MAX_WEIGHT):

  if not SACK:
    return 0

  MAX_VALUE = dict()
  MAX_VALUE[0] = 0

  for i in range(1,MAX_WEIGHT+1):

    value_list = [0]
    for id in SACK:
      (weight, val) = SACK[id]
      
      if weight <= i:
        value = val + MAX_VALUE[i - weight]
        value_list.append(value)

    MAX_VALUE[i] = max(value_list)

  return MAX_VALUE[MAX_WEIGHT]


def init_sack(WEIGHT, VALUE):
  SACK = dict()
  for idx in range(1,len(WEIGHT)+1):
    SACK[idx] = (WEIGHT[idx-1], VALUE[idx-1])
  return SACK

def max_value_memo(SACK, MAX_WEIGHT):
  CACHE = dict()
  return max_value_memo_aux(SACK, MAX_WEIGHT, CACHE)

def max_value_memo_aux(SACK, MAX_WEIGHT, CACHE):

  W_ID_LIST = tuple([x for x in SACK])
  if (W_ID_LIST, MAX_WEIGHT) in CACHE:
    return CACHE[(W_ID_LIST, MAX_WEIGHT)]

  value_list = [0]
  for id in SACK:
    (weight, val) = SACK[id]
    
    if weight <= MAX_WEIGHT:
      NEW_SACK = SACK.copy()
      del NEW_SACK[id]
      value = val + max_value_memo_aux(NEW_SACK, MAX_WEIGHT - weight, CACHE)
      value_list.append(value)

  max_value = max(value_list)
  CACHE[(W_ID_LIST, MAX_WEIGHT)] = max_value
  return max_value

WEIGHT = [  3,  5,  7,   9,  4,  10,  3,  2, 6, 1]
VALUE  = [100, 58, 88, 158, 33, 234, 23, 32, 1, 5]
SACK = init_sack(WEIGHT, VALUE)

MAX_WEIGHT = 165
print max_value_memo(SACK, MAX_WEIGHT)


print max_value(SACK, MAX_WEIGHT)
#print max_value_bottom_up(SACK, MAX_WEIGHT)
