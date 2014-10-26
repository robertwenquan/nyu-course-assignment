#!/usr/bin/python

def insertion_sort_dec(AA):

  n = len(AA)

  for i in range(1,n):
    key = AA[i]
    print ">> ", key

    for j in range(i-1,-1,-1):
      if (key > AA[j]):
        print "shift (%d) to the right" % (AA[j])
        AA[j+1] = AA[j]
        AA[j] = key
      else:
        break

    print AA


def insertion_sort_inc(AA):
  n = len(AA)

  for i in range(1,n):
    key = AA[i]
    print ">> ", key
    j = i-1
    while (j>=0 and key < AA[j]):
      print "shift (%d) to the right" % (AA[j])
      AA[j+1] = AA[j]
      j -= 1

    AA[j+1] = key

    print AA


print "decreasing sort:"
AA = [4, 5, 6, 3, 7]
print AA
insertion_sort_dec(AA)
print AA
print ""
print "increasing sort:"
print AA
insertion_sort_inc(AA)
print AA
