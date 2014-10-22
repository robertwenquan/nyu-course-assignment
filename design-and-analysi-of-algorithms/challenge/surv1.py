#!/usr/bin/python

import pprint

def make_dict(mm):
    mm[1].sort()

    newdict = dict()
    print(mm[1])
    for num in mm[1]:
        print(num)
        newdict[num] = 0

    print(newdict)

def in_range(point, range):
    if point >= range[0] and point <= range[1]:
        return True
    else:
        return False

def count_camera(cameras, roadpoints):

    result = []

    for point in m:
        result.append(0)
        for range in n:
            if in_range(point, range):
                result[-1] += 1

    return result

# this is stored in list
n = [[2, 5], [4, 8], [2, 6], [7, 11]]
m = [3, 4, 6.5, 12]

# this is stored in tuple
n = [1, 5], [2, 3], [3, 4]
m = [6, 5, 4, 3, 2, 1, 0]

pprint.pprint(count_camera(n, m))
