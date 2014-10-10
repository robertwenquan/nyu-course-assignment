#!/usr/bin/python

def f(x):
  return x**2

print f(8)

g = lambda x:x**2

print g(8)

def make_incrementor (n):
  return lambda x:x + n

f = make_incrementor(2)
g = make_incrementor(6)

print f(42), g(42)

# function based on another function
print make_incrementor(22)(33)

foo = [2, 18, 9, 22, 17, 24, 8, 12, 27]

print foo
print filter(lambda x:x % 3 == 0, foo)
print map(lambda x:x * 2 + 10, foo)
print reduce(lambda x,y:x+y, foo)

# find out prime numbers
n = 5000
nums = range(2, n) 
#print nums
for div in range(2,n-1):
  nums = filter(lambda x:x==div or x%div != 0, nums)
print nums


print map(lambda w: len(w), 'It is raining cats and dogs'.split())



import commands

lines = commands.getoutput('mount -v').splitlines()
points = [line.split()[2] for line in lines]
print points

print

#for line in lines:
#  print line.split()[2]

points = map(lambda line: line.split()[2], lines)
print points





