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

    self.game = GameEngine(False, ui_disabled = True)

  def filter(self, line):
    return True

  def prepare_game(self):
    self.game.north_player.intell_level = 2;
    self.game.south_player.intell_level = 2;

  def get_game_result(self, canvass):
    move_path, move_stats = self.game.north_player.whats_next_move()
    return (move_path, move_stats)

  def mapper1(self, _, line):
    if self.filter(line) == True:
      yield (None, line)

  def mapper2(self, _, line):
    optimal_path = self.get_game_result(line)

    yield ('xxxxxx', optimal_path)

  def steps(self):
    return [MRStep(mapper=self.mapper1),
            MRStep(mapper_init=self.prepare_game, mapper=self.mapper2)]

if __name__ == '__main__':
  MRCalculateOptimalPath.run()

