#!/usr/bin/python
#
# This is a sample unittest file for Player class
#

import unittest
from mock import *

from playcc import Player

class TestGameCanvass(unittest.TestCase):

  def setUp(self):
    self.bot_player = Player(robot = True, name = 'caicai', side = 'south')

  def test_init(self):
    self.assertEqual(self.bot_player.robot, True)
    self.assertEqual(self.bot_player.name, 'caicai')
    self.assertEqual(self.bot_player.side, 'south')
    self.assertEqual(self.bot_player.move_status, 'idle')
    self.assertEqual(self.bot_player.intell_level, 3)
    self.assertEqual(self.bot_player.select_loc, None)
    self.assertEqual(self.bot_player.select_path, [])
    self.assertEqual(self.bot_player.list_of_pieces, [(8,3), (8,4), (9,2), (9,3), (9,4), (9,5)])
    self.assertEqual(self.bot_player.castle_points, [(13, 3), (13, 4)])

  def test_remove_piece(self):
    pass

if __name__ == '__main__':
  unittest.main()

