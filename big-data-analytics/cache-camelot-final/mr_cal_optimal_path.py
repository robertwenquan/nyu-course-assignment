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
    '''
    This is the machine learned filter for the unrealistic/low probability
    canvass map scenarios
    It is to help eleminate the low probability cases in order to reserve
    cache space for the high probability cases
    '''
    return True

  def prepare_game(self):
    self.game.north_player.intell_level = 2;
    self.game.south_player.intell_level = 2;

  def get_game_result(self, mapkey):
    '''
    reset the game canvass with the mapkey
    and calculate the optimal next move
    '''

    canvass_map = self.key_to_canvass(mapkey)

    self.game.init_canvass_with_map(canvass_map)

    move_path, move_stats = self.game.north_player.whats_next_move()
    return (move_path, move_stats)

  def mapper1(self, _, line):
    '''
    This is the mapper function in step1
    It is to filter the low probability canvass scenarios
    '''
    if self.filter(line) == True:
      yield (None, line)

  def mapper2(self, _, mapkey):
    '''
    This is the mapper function in step2
    It is to transform the canvass map hashkey to real canvass 
    and calculate the optimal next move as well as the move statistics

    The result in this step is the final result of this MapReduce job
    '''

    optimal_path = self.get_game_result(mapkey)
    yield (mapkey, optimal_path)

  def steps(self):
    return [MRStep(mapper=self.mapper1),
            MRStep(mapper_init=self.prepare_game, mapper=self.mapper2)]

  def key_to_canvass(self, mapkey):
    '''
    hashkey representation of canvass to
    data structure in the game canvass

    INPUT: "404142434445X121314152132"
    OUTPUT: [[(4, 0), (4, 1), (4, 2), (4, 3), (4, 4), (4, 5)], \
             [(1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (3, 2)]]
    '''

    def unmap_loc(key):
      '''
      string to tuple representation of cell location

      INPUT1: '40'
      OUTPUT1: (4, 0)

      INPUT2: 'a3'
      OUTPUT2: (10, 3)
      '''
      off_x = int(key[0], 16)
      off_y = int(key[1], 16)
      return (off_x, off_y)

    north_pieces = []
    south_pieces = []

    for north_idx in range(0,6):
      north_piece = mapkey[north_idx * 2 : north_idx * 2 + 2]
      north_piece_loc = unmap_loc(north_piece)
      north_pieces.append(north_piece_loc)

    for south_idx in range(0,6):
      south_piece = mapkey[13 + south_idx * 2 : 13 + south_idx * 2 + 2]
      south_piece_loc = unmap_loc(south_piece)
      south_pieces.append(south_piece_loc)

    return [north_pieces, south_pieces]

if __name__ == '__main__':
  MRCalculateOptimalPath.run()

