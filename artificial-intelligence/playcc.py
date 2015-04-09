#!/usr/bin/python
#
# playcc.py
#
# this is the AI game
#

from pprint import pprint
from canvass import PlayGround

class Player():
  '''
  the AI game player
  '''

  # name of the player
  # default is 'aibot'
  name = 'robot'

  # intelligence level
  #  1 - low
  #  2 - medium
  #  3 - superhigh
  intell_level = 3

  def __init__(self, name = 'aibot'):

    if name == 'caicai':
      self.intell_level = 3
    elif name == 'tao1':
      self.intell_level = 2
    elif name == 'tao2':
      self.intell_level = 1

  def whats_next(self, canvass):
    '''
    from current situation, calculate what is next step
    input:  The Canvass
    output: ((x1,y1),(x2,y2))
            (x,y) cooridinate of the source cell
            (x,y) cooridinate of the detination cell
    '''

    x1 = 1
    y1 = 1
    x2 = 1
    y2 = 1

    return ((x1,y1),(x2,y2))

  def on_click(self, cell):
    print "click cell(%d,%d)" % (cell.x, cell.y)


#
# main game starts HERE
#

# setup the player
ai_player = Player('caicai')

# kick off the play ground
PG = PlayGround(player = ai_player)

