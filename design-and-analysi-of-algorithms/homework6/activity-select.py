#!/usr/bin/python

LIST = [[0,0],[1,4],[3,5],[0,6],[5,7],[3,9],[5,9],[6,10],[8,11],[8,12],[2,14],[13,16]]
N = len(LIST)

ACTIVITY = []
k = 0
for m in range(1,N):
  if LIST[m][0] >= LIST[k][1]:
    ACTIVITY.append(LIST[m])
    k = m
print ACTIVITY
