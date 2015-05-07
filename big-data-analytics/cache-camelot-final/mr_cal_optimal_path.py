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

class MRCalculateOptimalPath(MRJob):

  def __init__(self, args):

    super(MRCalculateOptimalPath, self).__init__(args)

  def mapper(self, _, line):

    print line

if __name__ == '__main__':
  MRCalculateOptimalPath.run()

