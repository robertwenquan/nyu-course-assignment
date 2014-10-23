#!/usr/bin/python

import random

__author__ = 'Wen'

def partition(AA, start, end):

    pivot = random.randint(start, end)
    AA[start], AA[pivot] = AA[pivot], AA[start]
    pivot = start

    pointA = start+1
    pointB = end

    while True:
        while (AA[pointB] > AA[pivot]):
            pointB -= 1
        if (pointB == pivot):
            break
        AA[pivot], AA[pointB] = AA[pointB], AA[pivot]
        pivot = pointB
        pointB -= 1

        while (AA[pointA] < AA[pivot]):
            pointA += 1
        if (pointA == pivot):
            break
        AA[pivot], AA[pointA] = AA[pointA], AA[pivot]
        pivot = pointA
        pointA += 1

    return pivot

def quick_sort(AA, start, end):

    # Here is a KEY point
    # if(start>end) is wrong!
    # has to be >=
    if (start >= end):
        return

    pivot = partition(AA, start, end)

    quick_sort(AA, start, pivot-1)
    quick_sort(AA, pivot+1, end)

AA = [3, 4, 3, 2, 6, 44, 22, 3, 1, 90]
quick_sort(AA, 0, len(AA)-1)
print (AA)

