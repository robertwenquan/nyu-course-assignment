#!/usr/bin/python
#
# mr_cal_optimal_path.py
#
# This is a map-reduce job to calculate optimal path for
# the mini camelot game
#

from tkui import *
from playcc import *
from mrjob.job import MRJob
from mrjob.job import MRStep

class MRCalculateOptimalPath(MRJob):

  def __init__(self, args):

    super(MRCalculateOptimalPath, self).__init__(args)

  def filter(self, line):
    return True

  def mapper1(self, _, line):
    if self.filter(line) == True:
      yield (None, line)

  def mapper2(self, _, line):
    yield ('xxxxxx', line)

  def steps(self):
    return [MRStep(mapper=self.mapper1),
            MRStep(mapper=self.mapper2)]

if __name__ == '__main__':
  MRCalculateOptimalPath.run()

