#!/usr/bin/python
#
# playcc.py
#
# this is the AI game
#

import sys
from pprint import pprint
from canvass import PlayGround

class Cell():
  '''
  one cell of the game canvass
  '''

  def __init__(self, x, y, status = 'disabled'):
    self.x = x
    self.y = y
    self.status = status
    self.selected = False

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

  # define the size of the game play ground
  ncol = 8
  nrow = 14

  canvass = dict()

  # who is playing?
  active_player = 'aibot'

  # selected_cell
  selected_cell = (-1,-1)

  # what is the playing doing?
  status = ''

  def __init__(self, player):
    self.player = player
    self.init_cells(self.ncol, self.nrow)
    self.ui = PlayGround(self)

    #configure(bg = "#234")

  def init_cells(self, ncol, nrow):
    '''
    initialize cell coordinates and state

    FIXME:
    this is a dirty initialization, with hard-coded cell selection
    an ideal one should be converting a visualized map like below to the desired cell map

    +--------+
    |xxx  xxx|
    |xx    xx|  x : disabled cells, not used in this map
    |x      x| ' ': free cells
    |        |  = : machine player
    |  ====  |  + : human player
    |   ==   |
    |        |
    |        |
    |   ++   |
    |  ++++  |
    |        |
    |x      x|
    |xx    xx|
    |xxx  xxx|
    +--------+

    '''
    
    # init all cells to 'free' state
    for i in range(nrow):
      for j in range(ncol):
        n = ncol*i + j

        cell = Cell(i,j,'free')
        self.canvass[n] = {'cell' : cell}

    # set the 'disabled' cells
    # these cells will be marked as "disabled" buttons
    for x,y in [ (0,0),  (0,1),  (0,2),  (0,5),  (0,6),  (0,7), \
                 (1,0),  (1,1),                  (1,6),  (1,7), \
                 (2,0),                                  (2,7), \
                (11,0),                                 (11,7), \
                (12,0), (12,1),                 (12,6), (12,7), \
                (13,0), (13,1), (13,2), (13,5), (13,6), (13,7)]:
      n = ncol*x + y
      self.canvass[n]['cell'].status = 'disabled'

    # set the robot play cells
    # these cells will be marked with 'blue' color
    for x,y in [(4,2), (4,3), (4,4), (4,5), \
                       (5,3), (5,4)]:
      n = ncol*x + y
      self.canvass[n]['cell'].status = 'play_bot'

    # set the human play cells
    # these cells will be marked with 'purple' color
    for x,y in [       (8,3), (8,4), \
                (9,2), (9,3), (9,4), (9,5)]:
      n = ncol*x + y
      self.canvass[n]['cell'].status = 'play_human'

  def print_debug_cell_map(self):
    '''
    print the ASCII cell map on the console
    for debugging purpose ONLY
    '''

    nrow = self.nrow
    ncol = self.ncol

    print '+--------+'
    for i in range(nrow):
      sys.stdout.write('|') 

      for j in range(ncol):
        n = ncol*i + j

        c_status = self.canvass[n]['cell'].status
        selected = self.canvass[n]['cell'].selected
        if c_status == 'disabled':
          sys.stdout.write('x')
        elif c_status == 'free':
          sys.stdout.write(' ')
        elif c_status == 'play_bot':
          if selected == True:
            sys.stdout.write('O')
          else:
            sys.stdout.write('=')
        elif c_status == 'play_human':
          if selected == True:
            sys.stdout.write('O')
          else:
            sys.stdout.write('+')

      print '|'
    print '+--------+'

  def update_cell_status(self, x, y, status, selected):
    '''
    update cell status according to x,y
    '''
    n = self.ncol * x + y
    cell = self.canvass[n]['cell']
    cell.status = status
    cell.selected = selected

  def start(self):
    self.ui.display()

  def on_click(self, x, y):
    '''
    handle the click event
    '''

    print "click cell(%d,%d)" % (x, y)
    n = self.ncol*x + y

    cell = self.canvass[n]['cell']
    if self.selected_cell == (-1,-1):
      if cell.selected == False and cell.status == 'play_human':
        cell.selected = True
        self.selected_cell = (x,y)
      elif cell.selected == False and cell.status != 'play_human':
        print 'you cannot select non-human cell to play'
      elif cell.selected == True:
        print 'BUG! Check your code!!!'
    else:

      # TODO caicai: check if it is a legitimate move
      # according to the game rule

      if cell.status == 'play_human' or cell.status == 'play_bot':
        print 'move to an empty cell!!!'
      elif cell.status == 'free' and cell.selected == False:
        x1, y1 = self.selected_cell
        x2, y2 = x, y

        self.update_cell_status(x1, y1, 'free', False)
        self.update_cell_status(x2, y2, 'play_human', False)
        self.selected_cell = (-1,-1)
      else:
        print 'BUG! Check your code!!!'

    self.print_debug_cell_map()
    
    self.ui.refresh_playground()
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

# setup the game with player
ai_player = Player('caicai')
game = GameEngine(ai_player)

# kick off the game with UI
game.start()

