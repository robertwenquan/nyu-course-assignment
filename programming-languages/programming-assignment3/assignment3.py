#!/usr/bin/python

import string


def F(n):
  if(n==0 or n==1 or n==2 or n==3):
    return 1

  NTH = dict()

  for i in range(0,4):
    NTH[i] = 1

  for i in range(4,n):
    NTH[i] = int((NTH[i-1]+NTH[i-2])*NTH[i-3]/NTH[i-4])

  result = int((NTH[n-1]+NTH[n-2])*NTH[n-3]/NTH[n-4])
  return result


def get_num(n):
  print F(n)


def sum_num(n):
  if n == 0:
    return 1
  else:
    return F(n) + sum_num(n-1)


def get_sum(n):
  print sum_num(n)


def get_bounds(n):
  print lower_bound(n)
  print upper_bound(n)


def upper_bound(n):
  i = 0

  while n >= F(i):
    i += 1

  return F(i)


def lower_bound(n):
  i = 0

  while F(i+1) < n:
    i += 1

  return F(i)


f_in  = open('/proc/self/fd/0', 'r')
f_out = open('/proc/self/fd/1', 'w')


# TODO: handle EOF
while True:
  line = string.replace(f_in.readline(), "\n", "")
  if (line == ""):
    print "ERR"
    break

  cmd_arr = string.split(line, " ")
  if len(cmd_arr) > 2:
    print "ERR"
    break

  CMD = cmd_arr[0]

  if (line == "QUIT"):
    break

  ARG = int(cmd_arr[1])

  if (CMD == "NTH"):
    get_num(ARG)
  elif (CMD == "SUM"):
    get_sum(ARG)
  elif (CMD == "BOUNDS"):
    get_bounds(ARG)
  else:
    print "ERR"
    break

