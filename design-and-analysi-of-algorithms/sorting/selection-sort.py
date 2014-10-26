#!/usr/bin/python

def selection_sort(AA):
  n = len(AA)

  for i in range(0,n-1):

    low = i
    for j in range(i,n):
      if (AA[j] < AA[low]):
        low = j
    
    print "new low is %d" % (AA[low])
    AA[low], AA[i] = AA[i], AA[low]
    print ">", AA

  print "last low %d is automatically ordered" % AA[i+1]

print "Selection sort example:"
A = [4, 5, 6, 3, 7]
print A
selection_sort(A)
print A
