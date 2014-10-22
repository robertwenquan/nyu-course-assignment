#!/usr/bin/python

__author__ = 'Quan Wen (robert.wen@nyu.edu)'

import pprint
import bisect

# This does almost the same as bisect.bisect_right(a, x, lo, hi)
# except the hi takes len(a)-1 rather than len(a)
def n_num_below_equal_using_bisec(list, num, start, end):

    if (start == end):
        if (num >= list[start]):
            return start+1
        else:
            return start

    mid = int((start + end)/2)

    if (num >= list[mid]):
        return n_num_below_equal_using_bisec(list, num, mid+1, end)
    else:
        return n_num_below_equal_using_bisec(list, num, start, mid)

# This does almost the same as bisect.bisect_left(a, x, lo, hi)
# except the hi takes len(a)-1 rather than len(a)
def n_num_below_using_bisec(list, num, start, end):

    if (start == end):
        if (num > list[start]):
            return start+1
        else:
            return start

    mid = int((start + end)/2)

    if (num > list[mid]):
        return n_num_below_using_bisec(list, num, mid+1, end)
    else:
        return n_num_below_using_bisec(list, num, start, mid)

def count_one_point(camera_list, point):
    # Here is a modified binary search, with T(n) = log(n)
    n_larger_than_low_bound = n_num_below_equal_using_bisec(camera_list['low_bound'], point, 0, len(camera_list['low_bound'])-1)
    # Here is another modified binary search, with T(n) = log(n)
    n_larger_than_high_bound = n_num_below_using_bisec(camera_list['high_bound'], point, 0, len(camera_list['high_bound'])-1)
    count = n_larger_than_low_bound - n_larger_than_high_bound
    # In total this function has O(2.log(n))
    return count

def count_camera(cameras, points):

    if (cameras[0] == 0):
        return [0 for point in points[1]]

    # create an associative array, with two attributes of array
    # O(n) for each attribute creation, so there are O(2n)
    # O(n.log(n)) for the sort of each array, so there are O(2n.log(n))
    # In total there are O(2n + 2.log(n)) in this code block
    camera_list = dict()
    camera_list['low_bound'] = sorted([cameras[idx][0] for idx in range(1,len(cameras))])
    camera_list['high_bound'] = sorted([cameras[idx][1] for idx in range(1,len(cameras))])

    # Here is a loop, iterating O(n) times.
    # The total amount of time will be O(n.T(n))
    # T(n) is in the count_one_point() function, which has O(2.log(n))
    results = []
    for point in points[1]:
        results.append(count_one_point(camera_list, point))

    # So in total this function has O(2n + 2n.log(n) + 2n.log(n)) = O(2n + 4n.log(n)) < O(n^2) = o(n^2)
    return results



#aa = [2, 2, 4, 7]
#print(n_num_below_equal_using_bisec(aa, 4, 0, 3))
#print(n_num_below_using_bisec(aa, 4, 0, 3))

#exit(0)

# test case1
n = 4, [2, 5], [4, 8], [2, 6], [7, 11]
m = 4, [3, 4, 6.5, 12]
expected = [2, 3, 1, 0]

result = count_camera(n, m)
if (result != expected):
    print("Bugged!! with result ", result)
    print("Expected result ", expected)
else:
    print(result)

# test case2
n = 3, [1, 5], [2, 3], [3, 4]
m = 7, [6, 5, 4, 3, 2, 1, 0]
expected = [0, 1, 2, 3, 2, 1, 0]

result = count_camera(n, m)
if (result != expected):
    print("Bugged!! with result ", result)
    print("Expected result ", expected)
else:
    print(result)

# test case3
n = 1, [2, 4]
m = 7, [1, 2, 3, 4, 5, 6, 7]
expected = [0, 1, 1, 1, 0, 0, 0]

result = count_camera(n, m)
if (result != expected):
    print("Bugged!! with result ", result)
    print("Expected result ", expected)
else:
    print(result)

n = 0, []
m = 7, [1, 2, 3, 4, 5, 6, 7]
expected = [0, 0, 0, 0, 0, 0, 0]
result = count_camera(n, m)
if (result != expected):
    print("Bugged!! with result ", result)
    print("Expected result ", expected)
else:
    print(result)
