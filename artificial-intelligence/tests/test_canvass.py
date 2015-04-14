#!/usr/bin/python
#
# This is a sample unittest file for GameCanvass class
# It verifies each class method from the QA point of view
#

import unittest
from mock import *

from playcc import GameCanvass

class TestGameCanvass(unittest.TestCase):

  nrow = 14
  ncol = 8

  def setUp(self):
    self.test_canvass = GameCanvass(self.nrow, self.ncol)

  def test_init(self):
    self.assertEqual(self.test_canvass.nrow, self.nrow)
    self.assertEqual(self.test_canvass.ncol, self.ncol)

    ncells = len(self.test_canvass.cells)
    self.assertEqual(ncells, self.nrow * self.ncol)

  def test_cell_map(self):
    '''
    verify there are 88 valid cells on the canvass
    verify the location of the disabled cells
    verify the north and south pieces location
    '''

    north_pieces_list =  [(4,2), (4,3), (4,4), (4,5), (5,3), (5,4)]
    south_pieces_list =  [(8,3), (8,4), (9,2), (9,3), (9,4), (9,5)]
    disabled_cell_list = [ (0,0),  (0,1),  (0,2),  (0,5),  (0,6),  (0,7), \
                           (1,0),  (1,1),                  (1,6),  (1,7), \
                           (2,0),                                  (2,7), \
                          (11,0),                                 (11,7), \
                          (12,0), (12,1),                 (12,6), (12,7), \
                          (13,0), (13,1), (13,2), (13,5), (13,6), (13,7)]

    n_valid_cells = 0
    for x in range(self.nrow):
      for y in range(self.ncol):
        cell = self.test_canvass.get_cell((x, y))

        if (x,y) in north_pieces_list:
          self.assertEqual(cell.status, 'north')
        elif (x,y) in south_pieces_list:
          self.assertEqual(cell.status, 'south')
        elif (x,y) in disabled_cell_list:
          self.assertEqual(cell.status, 'disabled')
        else:
          self.assertEqual(cell.status, 'free')

        if cell.status != 'disabled':
          n_valid_cells += 1

    self.assertEqual(n_valid_cells, 88)

  def test_get_cell(self):
    '''
    only valid (x,y) gets right cell
    cross check cell.x and cell.y whether it is the right cell
    for all invalid (x,y), None must be returned
    '''
    pass

  def test_move_cell(self):
    '''
    when one cell is moved, verify:
    1. original location becomes a free cell
    2. destinated location becomes an occupied cell
    3. the rest of the cells must remain unchanged
    '''
    pass

  def test_remove_cell(self):
    '''
    when one cell is removed from the canvass:
    1. only the specified cell gets removed
    2. the remaining cells must remain unchanged
    '''
    pass

  def test_add_cell(self):
    '''
    verify it
    '''
    pass

  def test_free_cell(self):
    '''
    verify it
    '''
    pass

  def test_reset_canvass(self):
    '''
    verify it
    '''
    pass

  def test_lock_canvass(self):
    '''
    verify only lock status is changed. All other status remains
    '''
    pass

  def test_unlock_canvass(self):
    '''
    verify only lock status is changed. All other status remains
    '''
    pass

if __name__ == '__main__':
  unittest.main()

