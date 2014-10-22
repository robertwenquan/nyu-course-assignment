#!/usr/bin/python

import pprint

def in_range(point, range):
    if point >= range[0] and point <= range[1]:
        return True
    else:
        return False

def count_camera(cameras, roadpoints):

    result = []

    for point in roadpoints[1]:
        result.append(0)
        for range in cameras:
            if (type(range) is not list):
                continue
            if in_range(point, range):
                result[-1] += 1

    return result

# this is stored in list
n = 4, [2, 5], [4, 8], [2, 6], [7, 11]
m = 4, [3, 4, 6.5, 12]

# this is stored in tuple
n = 3, [1, 5], [2, 3], [3, 4]
m = 7, [6, 5, 4, 3, 2, 1, 0]

pprint.pprint(count_camera(n, m))
