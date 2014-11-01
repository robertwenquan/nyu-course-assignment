#!/usr/bin/python

aa=[[1,2,3],[4,5,6],[5,6,7]]
print aa

aa=[]
b=[]
for i in range(4):
  a=[0 for i in range(10)]
  b.append(a)
    
print b

def xx():
  for i in range(5):
    yield i

a=xx()
print sum(a)

