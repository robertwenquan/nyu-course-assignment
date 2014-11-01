#!/usr/bin/python

__author__ = 'Quan Wen (robert.wen@nyu.edu)'


# This is the brute-force algorithm

def count_intersection(cables):
    lens = len(cables)

    cnt = 0
    for idx in range(1,lens):
        for prev_idx in range(0, idx):
            if (cables[idx] < cables[prev_idx]):
                cnt += 1

    return cnt

#
# complexity analysis
#
# It's a two level loop algorithm
# For a n elements list, the first level loops n-1 times
# For the second loop,
#  the 1st iteration loops 1 time, from range(0,1)
#  the 2nd iteration loops 2 times, from range(0,2)
#  ...
#  the i iteration loops i times, from range(0,i)
#  ...
#  the n-1 iteration loops n-1 times, from range(0,n-1)
#
#  So the total running time is SUM(1, 2, 3, ..., n-1)
#  T(n) = n.(n-1)/2
#  T(n) = O(n^2)

# absolutely we need a better running time.
# square is always not a good time

def test_it(test_data):

    for data in test_data:
        cables = data[0]
        expected = data[1]
        result = count_intersection(cables)

        if (result != expected):
            print("Buggy!!! with result ", result)
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
