#!/usr/bin/python
#
# playcc.py
#
# this is the AI game
#
#
#################################################################
# Basic goals
# TODO(cc): the legitimate move checking
# DONE(rw): game winning rule1 (catle point is taken)
# TODO(cc): game winning rule2 (all pieces are captured)
# TODO(cc): player logic
# TODO(rw): link the player to the game engine
# TODO(rw): reset game at any point, with confirmation.
# TODO(rw): end the game when winning condition is met.
#
#################################################################
# Stretching goals
# TODO(cc): intelligence level
# TODO(rw): choose intelligence level before game starts
#
#################################################################
# Aspirational goals (from software architecture point of view)
# TODO(cc): game hints: when the first cell is selected
#                       give hints about all legitimate moving destimation cells
# TODO(rw): integrate the game hints with UI hints
# TODO(cc): game point rule
# TODO(rw): unified logging
# TODO(rw): dettachable UI
# TODO(rw): notification via UI
# TODO(rw): cell initialization with human readable map
# TODO(rw): add student information in the footer of the application
# TODO(rw): add 'good' github link in the footer of the application
# TODO: Allow two robots playing together, meaning smart one(caicai) always wins the game
# TODO: Add game play header, with two player's name, level, etc.
# TODO: Add real-time timer and performance metrics for each play
# TODO: save game records
#
import sys
import getopt
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

class GameCanvass():
  '''
  This is the main data structure to define the game canvass matrix(14 x 8)
  Canvass is made of cells filled in rows and columns

  TODO: has not been integrated into the game engine yet
  '''

  def init_canvass(self):
    pass

  def lock_canvass(self):
    pass

  def reset_canvass(self):
    pass

  def move_cell(self):
    pass

  def remove_cell(self):
    pass

class Player():
  '''
  the AI game player

  attributes of one player:
  - list_of_pieces : a list of all active pieces(soldiers)
  - 
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

  # game canvass, data structure for the current board status
  canvass = dict()

  # define two players, only two players
  # human<->bot, bot<->human, bot<->bot, human<->human
  north_player = None
  south_player = None

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
    '''
    kickstart the game by calling the ui display
    '''
    self.ui.display()

  def on_click(self, x, y):
    '''
    handle the click event
    '''

    print "click cell(%d,%d)" % (x, y)
    n = self.ncol*x + y

    # find the selected cell
    cell = self.canvass[n]['cell']

    # this is to choose the cell to be moved
    if self.selected_cell == (-1,-1):
      if cell.selected == False and cell.status == 'play_human':
        cell.selected = True
        self.selected_cell = (x,y)
      elif cell.selected == False and cell.status != 'play_human':
        print 'you cannot select non-human cell to play'
      elif cell.selected == True:
        print 'BUG! Check your code!!!'
    # this is to choose the cell to move to.
    # in order to move here, it must be an empty cell on the canvass
    else:

      x1, y1 = self.selected_cell
      x2, y2 = x, y

      # check if it is a legitimate move according to the game rule
      # if not, do not move and throw warning
      if self.is_legitimate_move((x1, y1), (x2, y2)) == False:
        print "This is not a legitimate move. Please re-consider!"
        return

      if cell.status == 'play_human' or cell.status == 'play_bot':
        print 'move to an empty cell!!!'
      elif cell.status == 'free' and cell.selected == False:

        self.update_cell_status(x1, y1, 'free', False)
        self.update_cell_status(x2, y2, 'play_human', False)
        self.selected_cell = (-1,-1)
      else:
        print 'BUG! Check your code!!!'

    self.print_debug_cell_map()
    
    self.ui.refresh_playground()

    # check the game ending condition after the move of the human player
    win_the_game, who = self.is_match_end()
    if win_the_game == True:
      print "%s wins the game!! Ending game!!!" % who

  def is_match_point(self):
    '''
    THIS IS OPTIONAL
    Determine if it is approaching match point
    meaning one step further without defensive action will end the game

    Input: N/A (Check the global class canvass)
    Output: True / False
    '''
    return False

  def is_match_end(self):
    '''
    Determine whether the current condition is a match end
    meaning either the human player wins or the AI bot wins the game

    Game Winning Condition (meeting one wins the game)
    1. one side taking the position of the other side
    2. one side kills all cells of the other side

    Input: N/A (Check the global class canvass)
    Output: (result, who) result = True / False, who = "north" / "south"
    '''

    if self.is_castle_occupied("north") or self.is_all_pieces_dead("north"):
      # south wins the game
      # end the game with notification
      return True, "south"
    elif self.is_castle_occupied("south") or self.is_all_pieces_dead("south"):
      # north wins the game
      # end the game with notification
      return True, "north"

    return False, None

  def is_castle_occupied(self, side = "north"):
    '''
    Check if the castle of any side is occupied
    This is one of the game winning(end) rules

    Input: side = "north" or "south"
    Output: True / False

    north castle points: (0, 3), (0, 4)
    south castle points: (13, 3), (13, 4)
    '''

    if side == "north":
      castle_points = [(0, 3), (0, 4)]

      for x,y in castle_points:
        idx = x * self.ncol + y
        cell = self.canvass[idx]['cell']

        if cell.status == "play_human":
          return True

    elif side == "south":
      castle_points = [(13, 3), (13, 4)]

      for x,y in castle_points:
        idx = x * self.ncol + y
        cell = self.canvass[idx]['cell']

        if cell.status == "play_bot":
          return True

    return False

  def is_all_pieces_dead(self, side = "north"):
    '''
    Check if all pieces of any side are dead
    This is one of the game winning(end) rules

    Input: side = "north" or "south"
    Output: True / False
    '''
    return False

  def is_legitimate_leap(self, loc_start, loc_end, path):
    if loc_end in path:
      return 'is_illegal'

    x1, y1 = loc_start
    x2, y2 = loc_end

    if (abs(x2-x1)!=0 and abs(x2-x1)!=2) or (abs(y2-y1)!=0 or abs(y2-y1)!=2):
      return 'is_illegal'
    else:
      x = (x1+x2)/2
      y = (y1+y2)/2
      n = ncol*x+y
      cell = self.canvass[n]['cell']
      if cell.status == 'play_human':
        return 'is_legal'
      elif cell.status == 'play_bot':
        cell.update_cell_status(x,y, 'free', 'False')
        return 'is_legal'
      else:
        return 'is_illegal'

  def is_legitimate_first_move(self, loc_start, loc_end):
    x1, y1 = loc_start
    x2, y2 = loc_end

    if max(abs(x2-x1),abs(y2-y1))==1:
      return 'is_terminated'
    else:
      return self.is_legitimate_leap(loc_start,loc_end, [])

  def is_legitimate_move(self, loc_start, loc_end):
    '''
    Determine it is a legitimate move from (x1,y1) to (x2,y2)

    Input: loc_start: a tuple like (x, y)
           loc_end: a tuple like (x, y)
    Output: True / False
    '''
    x1, y1 = loc_start
    x2, y2 = loc_end

    idx1 = x1*self.ncol + y1
    idx2 = x2*self.ncol + y2

    print "Trying to move from (%d, %d)[idx %d] to (%d, %d)[idx %d]" % \
        (x1, y1, idx1, x2, y2, idx2)

    return True

  def legitimate_move_hints(self, cell_loc):
    '''
    THIS IS OPTIONAL
    Give hints about all possible moves
    When one cell is selected for possible move, we can predict all possible moves
    This will facilitate the human player to play the game with less thinking time...

    Input: cell_loc: it is a tuple like (x, y)
    Output: list_of_possible_moves: [(x1,y1), (x2,y2), (x3,y3)]
    '''

    x, y = cell_loc

    list_of_possible_moves = []

    return list_of_possible_moves

######################################################
# global functions start here
######################################################

def print_cmdline_help():
  '''
  command line helper
  '''
  print 'Command line help:'
  print '-h/--help       Print This Help'
  print '-v/--verbose    Verbose output, with debugging information'
  print '-n/--north      Set north player name'
  print '-s/--south      Set south player name'

def main(argv):
  '''
  main function
  arguments parsing, initialize players, and launch game with two players
  '''

  verbose = 0
  debug = 0
  player_north = ''
  player_south = ''

  try:
    opts, args = getopt.getopt(argv, 'hvdn:s:', ['help', 'verbose', 'debug', 'north=', 'south='])
  except getopt.GetoptError:
    print_cmdline_help()
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      print_cmdline_help()
      sys.exit()
    elif opt in ("-v", "--verbose"):
      verbose = 1
    elif opt in ("-d", "--debug"):
      debug = 1
    elif opt in ("-n", "--north"):
      player_north = arg
    elif opt in ("-s", "--south"):
      player_south = arg

  if debug == 1:
    print 'verbose = %d' % verbose
    print 'debug   = %d' % debug
    print 'player_north = %s' % player_north
    print 'player_south = %s' % player_south

  # setup the game with player
  ai_player = Player('caicai')
  game = GameEngine(ai_player)

  # kick off the game with UI
  game.start()

#
# command line execution starts from here
#
if __name__ == '__main__':
  main(sys.argv[1:])

