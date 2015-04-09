#!/usr/bin/python
#
# playcc.py
#
# this is the AI game
#

from pprint import pprint
from canvass import PlayGround
from Tkinter import *

class Player():
  '''
  the AI game player
  '''

  # name of the player
  # default is 'aibot'
  name = 'aibot'

  # intelligence level
  #  1 - low
  #  2 - medium
  #  3 - superhigh
  intell_level = 3

  def __init__(self, name = 'aibot', difficulty = 3):

    if name == 'caicai':
      self.intell_level = 3
    elif name == 'tao1':
      self.intell_level = 2
    elif name == 'tao2':
      self.intell_level = 1
    else:
      self.intell_level = difficulty

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


class GameEngine():
  '''
  Define the rules of the game
   - move rules
   - defeat rules
   - internal logic of the ganme
  '''

  player = None
  ui = None

  # who is playing?
  active_player = 'aibot'

  # what is the playing doing?
  status = ''

  def __init__(self, player):
    self.player = player
    self.ui = PlayGround(self)

    #configure(bg = "#234")

  def start(self):
    self.ui.display()

  def on_click(self, x, y):
    '''
    handle the click event

    '''
    print "click cell(%d,%d)" % (x, y)
    
    #button.configure(bg = "#234")

  def is_match_point():
    '''
    Determine if it is approaching match point
    meaning one step further will without defensive action will end the game
    '''
    pass

  def is_match_end():
    '''
    Determine whether the current condition is a match end
    meaning either the human player wins or the AI bot wins the game
    '''
    pass

  def is_legitimate_move(loc_start, loc_end):
    pass


#
# main game starts HERE
#

# setup the player
ai_player = Player('caicai')
game = GameEngine(ai_player)

# kick off the game
game.start()

