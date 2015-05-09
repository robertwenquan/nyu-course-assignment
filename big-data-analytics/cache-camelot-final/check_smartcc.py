#!/usr/bin/python

"""
check_smartcc.py

Check the smart cache for the game
and print out statistics for the cache entries for each difficulty level
"""

import pickle


cached_results = pickle.load(open('smartcc.cache', 'r'))

for level in [1,2,3]:
  for side in ['north', 'south']:
    print 'Level %d, %s: %d entries' % (level, side, len(cached_results[level][side]))
    for key in cached_results[level][side]:
      print key, cached_results[level][side][key]
