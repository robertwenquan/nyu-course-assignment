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


def integers():
    """Infinite sequence of integers."""
    i = 1
    while True:
        yield i
        i = i + 1

def squares():
    for i in integers():
        yield i * i

def take(n, seq):
    """Returns first n values from the given sequence."""
#    seq = iter(seq)
#    seq = seq
    result = []
    try:
      for i in range(n):
        result.append(seq.next())
    except StopIteration:
      pass
    return result


print take(6, squares()) # prints [1, 4, 9, 16, 25]





# basically defines a generator
def gen_numbers():
  i = 1
  while True:
    yield i
    i += 1

a = gen_numbers()
print a.next()
print a.next()

b = iter(gen_numbers())
print b.next()
print b.next()

print "generator expressions"

a = (x*x for x in range(1,10))
print a.next()
print a.next()
print a.next()
print "sum the rest of the list, not the whole list"
print sum(a)


# this is a verbose generator
# x*x + y*y == z*z
def abc():
  for x in range(1,100000):
    for y in range(1,100000):
      for z in range(1,10000):
        if x*x + y*y == z*z:
          yield (x,y,z)

# this is a really compact generator!!!!
pyt = ((x, y, z) for z in integers() for y in xrange(1, z) for x in range(1, y) if x*x + y*y == z*z)
print take(10, pyt)
#aaa = take(10, abc)
#aaa = abc()
#print aaa.next()
#print aaa.next()
#print aaa.next()


