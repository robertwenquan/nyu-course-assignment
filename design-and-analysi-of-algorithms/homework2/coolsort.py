#!/usr/bin/python

__author__ = 'Wen'

def ceiling(n):
    if (n == int(n)):
        return int(n)
    else:
        return int(n)+1

def cool_sort(AA, low, high):
    if (low == high):
        return
    elif (low+1 == high):
        if (AA[low] > AA[high]):
            AA[low], AA[high] = AA[high], AA[low]
    else:
        m = ceiling(2*(high-low+1)/3)

        range1_a, range1_b = low, low+m-1
        range2_a, range2_b = high-m+1, high
        range3_a, range3_b = low, low+m-1

        cool_sort(AA, range1_a, range1_b)
        cool_sort(AA, range2_a, range2_b)
        cool_sort(AA, range3_a, range3_b)

AA = [3, 4, 1, 2]
print(AA)
cool_sort(AA, 0, 3)
print(AA)

