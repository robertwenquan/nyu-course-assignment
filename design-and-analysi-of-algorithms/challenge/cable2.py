#!/usr/bin/python

import random
import pprint

__author__ = 'Quan Wen (robert.wen@nyu.edu)'

def partition(AA, start, end):

    cnt = 0

    pivot = random.randint(start, end)
    print("pivot: ", pivot)
    AA[start], AA[pivot] = AA[pivot], AA[start]
    if (AA[start] > AA[pivot]):
        cnt -= 1
    else:
        cnt += 1
    pivot = start

    pointA = start
    pointB = end

    while True:
        while (AA[pointB] > AA[pivot]):
            pointB -= 1
        if (pointB == pivot):
            break
        AA[pivot], AA[pointB] = AA[pointB], AA[pivot]
        cnt += 1
        pivot = pointB
        pointB -= 1

        while (AA[pointA] < AA[pivot]):
            pointA += 1
        if (pointA == pivot):
            break
        AA[pivot], AA[pointA] = AA[pointA], AA[pivot]
        cnt += 1
        pivot = pointA
        pointA += 1

    return pivot, cnt

def quick_sort(AA, start, end):

    # Here is a KEY point
    # if(start>end) is wrong!
    # has to be >=
    if (start >= end):
        return 0

    pivot, cnt = partition(AA, start, end)
    print ("COUNT par", cnt)

    cnt += quick_sort(AA, start, pivot-1)
    print ("COUNT +1", cnt)
    cnt += quick_sort(AA, pivot+1, end)
    print (">> COUNT +2", cnt)

    return cnt

def selection_sort(AA):

    cnt = 0
    n = len(AA)

    for idx in range(0,n-1):
        min = idx
        for i in range(idx+1, n):
            if (AA[i] < AA[min]):
                min = i
                cnt += 1
        AA[idx], AA[min] = AA[min], AA[idx]

    return cnt

def bubble_sort(AA):

    cnt = 0
    n = len(AA)

    for idx in range(n-1,0,-1):
        for i in range(0,idx):
            if (AA[i] > AA[i+1]):
                AA[i], AA[i+1] = AA[i+1], AA[i]
                cnt += 1

    return cnt

def count_intersection(cables):
    # doesn't work
    #return quick_sort(cables, 0, len(cables)-1)

    # work, but it's O(n*n)
    return bubble_sort(cables)

    # doesn't work
    #return selection_sort(cables)

def test_it(test_data):

    for data in test_data:
        cables = data[0]
        expected = data[1]
        result = count_intersection(cables)
        print(cables)

        if (result != expected):
            print("Buggy!!! with result ", result, " Expected result is ", expected)
        else:
            print(result)



test_data = []

cables = [2, 5, 1, 6, 4, 3]
expected = 7
test_data.append([cables, expected])

cables = [3, 2, 1]
expected = 3
test_data.append([cables, expected])

cables = [3, 2, 1]
expected = 3
test_data.append([cables, expected])

cables = [1, 2, 3, 4]
expected = 0
test_data.append([cables, expected])

cables = [1, 4, 2, 5, 3, 6]
expected = 3
test_data.append([cables, expected])

test_it(test_data)

