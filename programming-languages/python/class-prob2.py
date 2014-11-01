#!/usr/bin/python

class Bag:
  def __init__(self):
    self._b = set()
  def add(self, x):
    self._b = self._b.union({x})
  def addAll(self, xs):
    self._b = self._b.union(set(xs))
    #for x in xs:
    #  self.add(x)
  def contains(self, x):
    return x in self._b


class CountingBag(Bag):
  def __init__(self):
    Bag.__init__(self)
    self._n = 0

  def add(self, x):
    if not self.contains(x):
      self._n += 1
      Bag.add(self, x)

  def getNumItems(self):
    return self._n


myBag = CountingBag()
myBag.addAll([1,2,3,1,2,3])
numItems = myBag.getNumItems()

print numItems
