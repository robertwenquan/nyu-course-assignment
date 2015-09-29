#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
the most famous word count example for MRJob
"""

from mrjob.job import MRJob

class MRWordCount(MRJob):

  def mapper(self, key, line):
    for word in line.split():
      yield(word, 1)

  def reducer(self, key, items):
    cnt = 0
    for item in items:
      cnt += 1
    yield (key, cnt)

if __name__ == '__main__':
  MRWordCount.run()

