#!/usr/bin/python

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

