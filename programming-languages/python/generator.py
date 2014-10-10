#!/usr/bin/python

def simple_generator_function():
  for i in range(100):
    yield i*2

#for value in simple_generator_function():
#  print value

my_generator = simple_generator_function()
print next(my_generator)
print next(my_generator)
print next(my_generator)
print next(my_generator)

#for value in my_generator:
#  print value
