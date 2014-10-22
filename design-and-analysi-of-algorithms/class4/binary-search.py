#!/usr/bin/python

import pprint

# search the index
# if the number exists, return the index from the list
# if not, return -1

def find_num_binary_search(list, num, start, end):

    if (start == end):
        if (num == list[start]):
            return start
        else:
            return -1

    mid = int((start+end)/2)

    if (num > list[mid]):
        return find_num_binary_search(list, num, mid+1, end)
    else:
        return find_num_binary_search(list, num, start, mid)

    #
    # Why the following is incorrect!!! Think about it!!!
    #
    # Because mid for (0,1) is (0), mid-1 will be -1
    #
    # NEVER use (mid-1) when mid=(low+high)/2
    # ALWAYSE use (low, mid) and (mid+1, high) for the divide
    #

    #if (num < list[mid]):
    #    return find_num_binary_search(list, num, start, mid-1)
    #else:
    #    return find_num_binary_search(list, num, mid, end)


AA = [1, 3, 5, 66, 123, 133, 155, 234, 332, 345, 356, 376, 388, 456, 3242]

for idx in range(0,len(AA)):
    print("AA[", idx, "] = ", AA[idx])

print(find_num_binary_search(AA, 66, 0, len(AA)-1))
print(find_num_binary_search(AA, 234, 0, len(AA)-1))
print(find_num_binary_search(AA, 2334, 0, len(AA)-1))
print(find_num_binary_search(AA, 388, 0, len(AA)-1))