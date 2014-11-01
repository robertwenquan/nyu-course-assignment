#!/usr/bin/python

iterator = iter([2,3,4,5,6])

print iterator.next()
print iterator.next()
print iterator.next()

print "xxxxxxxxxxxxxxx line xxxxxxxxxxxxx"

class yrange:
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        return self

    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration()


y = yrange(3)
print y.next()
print y.next()
print y.next()

print list(yrange(5))
print sum(yrange(100))
print sum(xrange(100))

print list([1,2,3,4])
print list(iter([1,2,3,4]))
print sum([1,2,3,4])
print sum(iter([1,2,3,4]))


class zrange:
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return zrange_iter(self.n)

class zrange_iter:
    def __init__(self, n):
        self.i = 0
        self.n = n

    def __iter__(self):
        # Iterators are iterables too.
        # Adding this functions to make them so.
        return self

    def next(self):
        if self.i < self.n:
            i = self.i
            self.i += 1
            return i
        else:
            raise StopIteration()

y = yrange(5)
print y.next()
print y.next()
print list(y)
print list(y)

z = zrange(5)
#print z.next()   # no next
# every time it gives you an iterable, but it's not an iterator
# so you cannot call next()
print list(z)
print list(z)
print list(z)

zz = zrange_iter(5)
print list(zz)
print list(zz)
print list(zz)

class reverse_iter:
  def __init__(self, a):
    self.i = len(a) - 1
    self.aa = a

  def __iter__(self):
    return self

  def next(self):
    if (self.i >= 0):
      val = self.aa[self.i]
      self.i -= 1
      return val
    else:
      raise StopIteration()


print "try out new iterator here"

it = reverse_iter([1,2,3,4,76,5,3,33,5])
print it.next()
print it.next()
print it.next()
print it.next()
print it.next()
print it.next()
print it.next()
print it.next()
print it.next()
print it.next()
