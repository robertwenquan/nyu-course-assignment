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
from mrjob.protocol import JSONValueProtocol

class MRCalculateOptimalPath(MRJob):

  OUTPUT_PROTOCOL = JSONValueProtocol

  def __init__(self, args):

    super(MRCalculateOptimalPath, self).__init__(args)
    self.game = GameEngine(True, ui_disabled = True)

  """
  MRJOB SPECIFIC FUNCTIONS
  """
  def mapper1(self, _, mapkey):
    '''
    This is the mapper function in step1
    It is to filter the low probability canvass scenarios
    '''
    if self.filter(mapkey) == True:
      yield (None, (mapkey, 1, 'north'))
      yield (None, (mapkey, 1, 'south'))
      yield (None, (mapkey, 2, 'north'))
      yield (None, (mapkey, 2, 'south'))
      yield (None, (mapkey, 3, 'north'))
      yield (None, (mapkey, 3, 'south'))

  def mapper2(self, _, request):
    '''
    This is the mapper function in step2
    It is to transform the canvass map hashkey to real canvass 
    and calculate the optimal next move as well as the move statistics

    The result in this step is the final result of this MapReduce job
    '''

    mapkey, level, side = request

    if self.validate_mapkey(mapkey) == False or \
        level < 1 or level > 3 or \
        side != 'north' and side != 'south':
      return

    optimal_path = self.get_game_result(mapkey, level, side)
    yield (mapkey, (level, side, optimal_path))

  def reducer(self, key, results):
    '''
    This is the reducer function in step2
    It is to combine the results for all levels and sides into a single dictionary
    and return as a JSON string
    '''

    entry = dict()
    entry[key] = dict()
    entry[key][1] = { 'north' : {}, 'south' : {} }
    entry[key][2] = { 'north' : {}, 'south' : {} }
    entry[key][3] = { 'north' : {}, 'south' : {} }

    for result in results:
      level, side, path = result
      entry[key][level][side] = path

    yield key, entry

  def steps(self):
    return [MRStep(mapper=self.mapper1),
            MRStep(mapper=self.mapper2, reducer=self.reducer)]


  """
  NON MRJOB SPECIFIC FUNCTIONS
  """
  def filter(self, line):
    '''
    This is the machine learned filter for the unrealistic/low probability
    canvass map scenarios
    It is to help eleminate the low probability cases in order to reserve
    cache space for the high probability cases
    '''
    return True

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

      if north_piece_loc != (0, 0):
        north_pieces.append(north_piece_loc)

    for south_idx in range(0,6):
      south_piece = mapkey[13 + south_idx * 2 : 13 + south_idx * 2 + 2]
      south_piece_loc = unmap_loc(south_piece)

      if south_piece_loc != (0, 0):
        south_pieces.append(south_piece_loc)

    return [north_pieces, south_pieces]

  def get_game_result(self, mapkey, level, side):
    '''
    reset the game canvass with the mapkey
    and calculate the optimal next move
    '''

    time_start = time.time()

    # reset canvass map
    self.game.init_canvass_with_mapkey(mapkey)

    # reset difficulty level
    self.game.north_player.intell_level = level;
    self.game.south_player.intell_level = level;

    # calculate results
    if side == 'north':
      move_path, move_stats = self.game.north_player.whats_next_move()
    else:
      move_path, move_stats = self.game.south_player.whats_next_move()

    mapkey_list_over_path = self.game.get_maphash_list_over_path(mapkey, move_path, side)

    time_end = time.time()
    time_elapsed = time_end - time_start

    return (move_path, move_stats, mapkey_list_over_path, time_elapsed)

  def validate_mapkey(self, mapkey):
    '''
    validate canvass map hashkey
    '''
    if len(mapkey) != 25:
      return False

    return True

if __name__ == '__main__':
  MRCalculateOptimalPath.run()

