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

def concat(left, right):
  return (left[0] + right[0], left[1] + right[1])

def get_max(lists):
  if not lists:
    return (0,[])

  lists = sorted(lists, key=lambda aaa: aaa[0], reverse=True)
  return lists[0]

def max_value_memo_with_lists(SACK, MAX_WEIGHT):
  CACHE = dict()
  return max_value_memo_aux(SACK, MAX_WEIGHT, CACHE)

def max_value_memo_aux(SACK, MAX_WEIGHT, CACHE):

  W_ID_LIST = tuple([x for x in SACK])
  if (W_ID_LIST, MAX_WEIGHT) in CACHE:
    return CACHE[(W_ID_LIST, MAX_WEIGHT)]

  value_list = []
  for id in SACK:
    (weight, val) = SACK[id]
    
    if weight <= MAX_WEIGHT:
      NEW_SACK = SACK.copy()
      del NEW_SACK[id]
      (value,lists) = concat((val,[id]), max_value_memo_aux(NEW_SACK, MAX_WEIGHT - weight, CACHE))
      value_list.append((value,lists))

  (max_value,max_list) = get_max(value_list)
  CACHE[(W_ID_LIST, MAX_WEIGHT)] = (max_value, max_list)
  return (max_value, max_list)

WEIGHT = [  3,  5,  7,   9,  4,  10,  3,  2, 6, 1]
VALUE  = [100, 58, 88, 158, 33, 234, 23, 32, 1, 5]
SACK = init_sack(WEIGHT, VALUE)

MAX_WEIGHT = 25
print max_value_memo_with_lists(SACK, MAX_WEIGHT)

#print max_value(SACK, MAX_WEIGHT)
#print max_value_bottom_up(SACK, MAX_WEIGHT)
