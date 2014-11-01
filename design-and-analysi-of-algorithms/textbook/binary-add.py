#!/usr/bin/python

def reverse_bit(AA):
  n = len(AA)
  for idx in range(n-1,-1,-1):
    yield AA[idx]
  
def binary_add(AA, BB, CC):
  carry = 0

  n = len(AA)
  for bit in range(0,n):
    CC[bit] = (AA[bit] + BB[bit] + carry) % 2
    carry = (AA[bit] + BB[bit] + carry) / 2

  CC[bit+1] = carry

AA = [0, 1, 1, 0, 1, 1, 1, 1]
BB = [1, 1, 0, 0, 0, 1, 1, 0]
CC = [0 for i in range(0,9)]

print ">>"
#print "  ", AA
print "  ", [i for i in reverse_bit(AA)]
print ">>"
#print "  ", BB
print "+ ", [i for i in reverse_bit(BB)]
print ">>"
binary_add(AA, BB, CC)
print [i for i in reverse_bit(CC)]
