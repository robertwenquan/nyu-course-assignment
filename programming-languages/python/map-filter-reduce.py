#!/usr/bin/python

print map(lambda x: x*2, [1,2,3])

print filter(lambda x: x>6, [1,3,5,7,9])
print filter(lambda x: x!='A', "ABBAC")

print reduce((lambda x, y: x * y), [1, 2, 3, 4])

