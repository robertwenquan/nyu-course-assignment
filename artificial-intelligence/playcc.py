#!/usr/bin/python
#
# playcc.py
#
# this is the AI game
#
# pylint: disable=fixme, disable=todo
#
#################################################################
# Basic goals
#
# TODO: DONE game canvass with cell display
# TODO: DONE cell free move without checking
# TODO: DONE the legitimate plain move checking
# TODO: DONE the legitimate leap move checking
# TODO: DONE stupid sample player (for integration)
# TODO: DONE player logic
# TODO: DONE game winning rule1 (catle point is taken)
# TODO: DONE game winning rule2 (all pieces are captured)
# TODO: DONE link the player to the game engine
# TODO: DONE reset game at any point, with confirmation.
# TODO: DONE end the game when winning condition is met.
# TODO(rw): white(north) always starts first
# TODO(rw): choose side for human player
# TODO(rw): choose side on the UI
# TODO(rw): performance metrics interface definition
# TODO(rw): expose performance metrics to UI for each move
# TODO(cc): record performance metrics for each move
# TODO(rw): unselect a cell when it was chosen by mistake
#
#################################################################
# Stretching goals
#
# TODO: DONE intelligence level
# TODO(rw): choose intelligence level before game starts, on UI
# TODO(rw): rollback and forward
#
#################################################################
# Aspirational goals (from software architecture and ease point of view)
#
# TODO(rw): unified logging
# TODO(rw): notification via UI
# TODO(cc): add student information in the footer of the application
# TODO(cc): add about box with 'good' github link in the footer
# TODO(cc): game hints: when the first cell is selected
#                       give hints about all legitimate moving destimation
# TODO(rw): integrate the game hints with UI hints
# TODO(rw): dettachable UI
# TODO(rw): cell initialization with human readable map
# TODO: Allow two robots playing together
# TODO: Add game play header, with two player's name, level, etc.
# TODO: Add real-time timer and performance metrics for each play
# TODO: save game records
#
#################################################################
# Bugs
#
# FIXME(rw): UI doesn't refresh in the callback function
# FIXME(rw): on Mac, cell background color is not shown
# FIXME(rw): on Mac, menu is not shown
# FIXME(cc): FIXED one piece, game point not win
# FIXME(cc): two pieces, game point not win but approaching the further piece
#

import sys
import time
import getopt
from copy import copy
from pprint import pprint
from tkui import PlayGround


class Cell(object):
  '''
  one cell of the game canvass
  '''

  def __init__(self, x, y, status = 'disabled'):
    self.x = x
    self.y = y
    self.status = status
    self.selected = False
    self.lock = False


class GameCanvass(object):
  '''
  This is the main data structure to define the game canvass matrix(14 x 8)
  Canvass is made of cells filled in rows and columns
  '''

  def __init__(self, nrow, ncol):

    self.nrow = nrow
    self.ncol = ncol

    self.cells = dict()
    self.init_canvass(nrow, ncol)

  def init_canvass(self, nrow, ncol):
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
    for x in range(nrow):
      for y in range(ncol):

        n = ncol*x + y

        cell = Cell(x,y,'free')
        self.cells[n] = cell

    # set the 'disabled' cells
    # these cells will be marked as "disabled" buttons
    for x,y in [ (0,0),  (0,1),  (0,2),  (0,5),  (0,6),  (0,7), \
                 (1,0),  (1,1),                  (1,6),  (1,7), \
                 (2,0),                                  (2,7), \
                (11,0),                                 (11,7), \
                (12,0), (12,1),                 (12,6), (12,7), \
                (13,0), (13,1), (13,2), (13,5), (13,6), (13,7)]:
      n = ncol*x + y
      self.cells[n].status = 'disabled'

    # set the north player cells
    # these cells will be marked with 'blue' color
    for x,y in [(4,2), (4,3), (4,4), (4,5), \
                       (5,3), (5,4)]:
      n = ncol*x + y
      self.cells[n].status = 'north'

    # set the south player cells
    # these cells will be marked with 'purple' color
    for x,y in [       (8,3), (8,4), \
                (9,2), (9,3), (9,4), (9,5)]:
      n = ncol*x + y
      self.cells[n].status = 'south'

  def lock_canvass(self):
    '''
    lock all celss when game ends
    '''
    nrow = self.nrow
    ncol = self.ncol

    for x in range(nrow):
      for y in range(ncol):
        cell = self.get_cell((x,y))
        cell.lock = True

  def unlock_canvass(self):
    '''
    unlock all cells when game is reset
    '''
    nrow = self.nrow
    ncol = self.ncol

    for x in range(nrow):
      for y in range(ncol):
        cell = self.get_cell((x,y))
        cell.lock = False

  def reset_canvass(self):
    '''
    when the game is reset, the canvass needs to be reset to initial state
    '''
    self.cells = dict()
    self.init_canvass(self.nrow, self.ncol)

  def free_cell(self, loc):
    '''
    set the cell free
    '''
    cell = self.get_cell(loc)
    if cell == None:
      print 'Error!'
      return

    cell.status = 'free'
    cell.selected = False
    cell.lock = False

  def move_cell(self, loc_start, loc_end):
    '''
    move one cell from one location to another
    '''
    cell_from = self.get_cell(loc_start)
    cell_to   = self.get_cell(loc_end)
    if cell_from == None or cell_to == None:
      print 'Error!'
      return

    cell_to.status = cell_from.status
    cell_to.selected = cell_from.selected
    cell_to.lock = cell_from.lock

    self.free_cell(loc_start)

  def remove_cell(self, loc):
    self.free_cell(loc)

  def add_cell(self, loc, side):
    cell = self.get_cell(loc)
    cell.status = side
    cell.selected = False
    cell.lock = False

  def get_cell(self, loc):
    '''
    get the cell object according to x,y coordinates
    return None if cell is not found
    '''
    x, y = loc

    # validate (x, y)
    # e.g    for (2, 7), n = 8*2 + 7 = 23
    #       also (3,-1), n = 8*3 - 1 = 23
    # cell[23] is valid but (3, -1) is not
    if x < 0 or x > self.nrow-1 or y < 0 or y > self.ncol-1:
      return None

    idx = self.ncol * x + y
    return self.cells.get(idx, None)
    
  def get_adjacent_cell_list(self, loc, query_type_blacklist):
    '''
    get the adjacent cell list based on a type check BLACKLIST

    NORMALLY there are 8 adjacent cells surrounding the (x,y)
    BUT in the border area, some of the 8 cells might be non-existing and should be excluded
    IN SOME OTHER CASES, we dont want 'disabled' cells, or 'free' cells, so we have a query blacklist

    loc: (x,y) location of the cell
    query_type_blacklist: [] get all valid adjacent cells in a list
                          ['disabled', 'free'], to exclude 'disabled' and 'free' cells from the adjacent cells
                          ['disabled'], only exclude 'disabled' cells from the adjacent cells
    '''
    x, y = loc
    adjacent_cells = [(x-1,y-1),(x-1,y),(x-1,y+1), \
                      (x  ,y-1),        (x  ,y+1), \
                      (x+1,y-1),(x+1,y),(x+1,y+1)]

    adjacent_cell_list = []

    for cell_loc in adjacent_cells:
      cell = self.get_cell(cell_loc)

      # never retrive non-existing cells
      if cell == None:
        continue

      # if query type is not specified, don't check cell status
      if query_type_blacklist == []:
        adjacent_cell_list.append(cell_loc)
        continue

      # otherwise, only add cell status that not matches query list
      if cell.status not in query_type_blacklist:
        adjacent_cell_list.append(cell_loc)

    return adjacent_cell_list

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

        c_status = self.get_cell((i,j)).status
        selected = self.get_cell((i,j)).selected
        if c_status == 'disabled':
          sys.stdout.write('x')
        elif c_status == 'free':
          sys.stdout.write(' ')
        elif c_status == 'north':
          if selected == True:
            sys.stdout.write('O')
          else:
            sys.stdout.write('=')
        elif c_status == 'south':
          if selected == True:
            sys.stdout.write('O')
          else:
            sys.stdout.write('+')

      print '|'
    print '+--------+'


class Player(object):
  '''
  the AI game player

  common attributes:
  ------------------
  - robot          : True/False
  - name           : a human readable name of the player
  - side           : 'north' or 'south'
  - move_status    : intermediate status ['idle', 'selected', 'hopped']
  - list_of_pieces : a list of all active pieces(soldiers)
  - castle_points  : castle points of this side
  - rival          : the opponent player
  - canvass        : the global canvass view

  robot attributes :
  ------------------
  - intell_level   : the intelligence level (1,2,3), the higher the smarter
  - 
  '''

  robot = True
  name = 'aibot'
  side = 'north'

  move_status = 'idle'
  select_loc = None
  select_path = []

  list_of_pieces = []

  def __init__(self, robot = True, name = 'aibot', side = '', move_status = 'idle', difficulty = 3):

    self.robot = robot
    self.name = name
    self.side = side
    self.move_status = move_status

    if self.name == 'caicai':
      self.intell_level = 3
    elif self.name == 'tao1':
      self.intell_level = 2
    elif self.name == 'tao2':
      self.intell_level = 1
    else:
      self.intell_level = difficulty

    self.init_pieces()
    self.init_castle_points()

  def reset_player(self):
    '''
    This is for the game reset
    reset all player info to the initial state
    '''
    self.init_pieces()
    self.move_status = 'idle'
    self.select_loc = None
    self.select_path = []

  def init_pieces(self):
    '''
      initialize the pieces of this player
      north player and south player has different default pieces locations
    '''

    if self.side == 'north':
      self.list_of_pieces = [(4,2), (4,3), (4,4), (4,5), (5,3), (5,4)]
    elif self.side == 'south':
      self.list_of_pieces = [(8,3), (8,4), (9,2), (9,3), (9,4), (9,5)]
    else:
      print 'BUG: Check your code!!!'
      exit(55)

  def init_castle_points(self):
    '''
      initialize the castle points of one player
      north player and south play has different castle points
    '''

    if self.side == 'north':
      self.castle_points = [(0, 3), (0, 4)]
    elif self.side == 'south':
      self.castle_points = [(13, 3), (13, 4)]
    else:
      print 'BUG: Check your code!!!'
      exit(55)

  def select_piece(self, loc):
    self.select_loc = loc

  def add_cell_to_select_path(self, loc):
    self.select_path.append(loc)

  def clear_select_path(self):
    self.select_path = []

  def set_rival(self, rival):
    self.rival = rival

  def set_canvass(self, canvass):
    self.canvass = canvass

  def set_game(self, game):
    self.game = game

  def is_self_piece(self, loc):
    '''
    Input:
      loc is a tuple like (x,y)
    Return Value:
      True/False - whether this location is a valid piece for this player
    '''
    return loc in self.list_of_pieces

  def move_piece(self, loc_from, loc_to):
    '''
    move one piece from loc1 to loc2
    update player piece info as well as canvass map
    '''
    self.list_of_pieces.remove(loc_from)
    self.list_of_pieces.append(loc_to)
    self.canvass.move_cell(loc_from, loc_to)

  def remove_piece(self, location):
    '''
    remove one piece from the canvass
    '''
    self.list_of_pieces.remove(location)
    self.canvass.remove_cell(location)

  def add_piece(self, location):
    '''
    add one piece to the canvass
    '''
    self.list_of_pieces.append(location)
    self.canvass.add_cell(location, self.side)

  def whats_next_move(self):
    '''
    from current canvass situation, calculate what is next step
    input:  
    output: [(x1,y1),(x2,y2),(x3,y3),...]
    '''
    #TODO(cc): fix bugs when value of level is big

    maximum_value = -300
    optimum_path = []
    best_move = (-1,-1)
    alpha = -300
    beta = 300
    level = 1 

    maximum_value, best_piece, optimum_action = self.max_value(level, alpha, beta)
    optimum_path.append(best_piece)
    for step in optimum_action:
      optimum_path.append(step)

    max_depth_reached = 11
    nodes_generated = 22
    num_pruning_max_value = 33
    num_pruning_min_value = 44
    move_statistics = (max_depth_reached, nodes_generated, num_pruning_max_value, num_pruning_min_value)

    return optimum_path, move_statistics

  def max_value(self, level, alpha, beta):
    '''
    Help robot to find the optimal action
    '''
    win_the_game, who = self.game.is_match_end()
    if win_the_game == True:
      if who == self.side:
        return 300, (), []
      else:
        return -300, (), []
    if level == 0:
      return self.estimate_function(),(),[] 
    level -= 1
    maximum_value = -300
    optimum_path = []
    best_piece = self.list_of_pieces[-1] 
    copy_pieces = copy(self.list_of_pieces)

    for piece in copy_pieces:
      actions = self.possible_action(piece,self)
      for path in actions:
        pending_set = self.action_simulation(self,piece,path)
        v_min, best, path_min = self.min_value(level, alpha, beta)
        self.simulation_recovery(self.rival,piece,path,pending_set)
        if v_min > maximum_value:
          maximum_value = v_min
          best_piece = piece
          optimum_path = path
        if v_min>= beta:
          return maximum_value, best_piece, optimum_path
        alpha = max(alpha,maximum_value)
    return maximum_value, best_piece, optimum_path

  def min_value(self, level, alpha, beta):
    '''
    Calculate best solution of rival player
    '''
    win_the_game, who = self.game.is_match_end()
    if win_the_game == True:
      if who == self.side:
        return 300, (), []
      else:
        return -300, (), []
    
    if level == 0:
      return self.estimate_function(), (), []
    level -= 1
    minimum_value = 300
    optimum_path = []
    best_piece = self.rival.list_of_pieces[-1] 
    
    copy_pieces = copy(self.rival.list_of_pieces)
    for piece in copy_pieces:
      actions = self.possible_action(piece,self.rival)
      for path in actions:
        pending_set = self.action_simulation(self.rival, piece,path)
        v_max, best, path_max = self.max_value(level, alpha, beta)
        self.simulation_recovery(self,piece,path,pending_set)
        if v_max < minimum_value:
          minimum_value = v_max
          best_piece = piece
          optimum_path = path
        if v_max<= alpha:
          return minimum_value, best_piece, optimum_path
        beta = min(beta,minimum_value)
    return minimum_value, best_piece, optimum_path

  def action_simulation(self,player,piece,path):
    '''
    simulate action of every possibility
    '''
    x, y = piece
    pending_set = []
   
    for cell in path:
      x1, y1 = cell
      if max(abs(x1-x),abs(y1-y)) == 1:
        player.move_piece((x,y),(x1,y1))
        return []
      else:
        player.move_piece((x,y),(x1,y1))
        cell = self.canvass.get_cell(((x+x1)/2,(y+y1)/2))
        if cell.status != player.side:
          player.rival.remove_piece(((x+x1)/2,(y+y1)/2))
          pending_set.append(((x+x1)/2,(y+y1)/2))
        x = x1
        y = y1
    return pending_set
  
  def simulation_recovery(self, player, piece,path,pending_set):
    '''
    Recover simulated canvass to original one
    '''
    for cell in pending_set:
      player.add_piece(cell)
    player.rival.move_piece(path[-1],piece)

  def possible_action(self, piece,player):
    '''
    Calculate every possible of each piece
    Input: available piece
    Output: all possible path of this piece
    '''
    x, y = piece
    possible_move = []
    adjacent_cell_list = self.canvass.get_adjacent_cell_list((x,y), ['disabled'])
    for (a,b) in adjacent_cell_list:
      cell = self.canvass.get_cell((a,b))
      if cell.status == 'free':
        possible_move.append([(a,b)])
      else:
        xx = 2*a-x
        yy = 2*b-y
        cell_to = self.canvass.get_cell((xx,yy))
        if cell_to == None:
          continue
        if cell_to.status == 'free':
          ret = self.possible_jump((xx,yy),player, [], [(x,y)], [(a,b)])
          for path in ret:
            possible_move.append(path)
    return possible_move

  def possible_jump(self, cell_loc, player, current_path, explored_set, pending_set):
    '''
    Calculate all possible path for a cell to move, is used for robot to choose the best move.

    Input: cell_loc: a tuple like (x,y)
           current_path: the path from original path to current cell
           explored_set: all cell expeared on the path
           pending_set: enemy piece that have been captured
    Output: pathes reached this piece and moving on
    '''

    #TODO(cc): find the reason why it reaches the limitaion of recurssion times

    x, y = cell_loc
    explored_set.append((x,y))
    current_path.append((x,y))
    return_path = [current_path]

    adjacent_cell_list = self.canvass.get_adjacent_cell_list((x,y), ['disabled', 'free'])
    for (a,b) in adjacent_cell_list:

      if (a,b) in pending_set:
        continue

      cell = self.canvass.get_cell((a,b))

      xx = x + (a-x)*2
      yy = y + (b-y)*2
      if (xx,yy) in explored_set:
        continue

      # TODO: since there are a lot of get and check, 
      # better to write a function like check_cell_status('free') = True/False
      # if you want to write it, write it
      cell_to = self.canvass.get_cell((xx,yy))
      if cell_to == None:
        continue

      if cell_to.status == 'free':
        pending = copy(pending_set)
        if cell.status == player.rival.side:
          pending.append((a,b))
        path = copy(current_path)
        ret = self.possible_jump((xx,yy), player, path, explored_set, pending )
        #print 'path', path
        #print 'ret', ret
        #for path in ret:
        #  return_path.append(path)
        return_path += ret

    return return_path

  def estimate_function(self):
    '''
    Estimate utility based on current canvass to help player make decision
    '''
    max = 0
    min = 0
    number_of_adjacent = 0    
    for piece in self.list_of_pieces:
      x, y = piece
      adjacent_cell_list = self.canvass.get_adjacent_cell_list((x,y), [])
      for (a,b) in adjacent_cell_list:
        cell = self.canvass.get_cell((a,b))
        if cell.status == self.rival.side:
          number_of_adjacent += 1

    if self.side == 'south':
      for piece in self.list_of_pieces:
        x, y = piece
        max += (14-x)*(14-x)
      for piece in self.rival.list_of_pieces:
        x, y = piece
        min += (x+1)*(x+1)
    elif self.side == 'north':
      for piece in self.list_of_pieces:
        x, y = piece
        max += (x+1)*(x+1)
      for piece in self.rival.list_of_pieces:
        x, y = piece
        min += (14-x)*(14-x)
    else:
      print 'BUG: check your code!'
      exit(55)

    return (max-min)/6+30*(len(self.list_of_pieces)-len(self.rival.list_of_pieces))+-30*number_of_adjacent

class GameEngine(object):
  '''
  Define the rules of the game
   - move rules
   - defeat rules
   - internal logic of the ganme
  '''

  # define the size of the game play ground
  ncol = 8
  nrow = 14

  # define two players, only two players
  # human<->bot, bot<->human, bot<->bot, human<->human
  north_player = None
  south_player = None

  # who is actively playing?
  active_player = None

  # selected_cell
  selected_cell = (-1,-1)

  # what is the playing doing?
  status = ''

  def __init__(self, player1, player2):

    for player in [player1, player2]:
      print player.robot
      print player.name
      if player.side == 'north':
        self.north_player = player
      elif player.side == 'south':
        self.south_player = player

    if self.north_player == None or self.south_player == None:
      print 'Not enough player to play! Please check configuration!'
      exit(54)

    # if human player exists, human plays first
    # otherwise north plays first
    self.active_player = self.get_human_player()
    if self.active_player == None:
      self.active_player = self.north_player

    self.canvass = GameCanvass(self.nrow, self.ncol)

    # set rival to players
    self.north_player.set_rival(self.south_player)
    self.south_player.set_rival(self.north_player)

    # set canvass to players
    self.north_player.set_canvass(self.canvass)
    self.south_player.set_canvass(self.canvass)

    # set game to players
    self.north_player.set_game(self)
    self.south_player.set_game(self)

    # initialize UI
    self.ui = PlayGround(self)

  def reset_game(self):
    '''
    reset the game canvass to default
    '''
    print 'resetting the game...'
    self.canvass.reset_canvass()
    self.north_player.reset_player()
    self.south_player.reset_player()

    self.canvass.print_debug_cell_map()

    self.canvass.unlock_canvass()

    self.ui.reset_ui()
    self.ui.refresh_playground()

  def about_me(self):
    print 'about me...'

  def get_human_player(self):
    '''
    return the human player object
    limit: there is at most one human player in the game
           there is possibility no human player is available in the game
    '''
    for player in [self.north_player, self.south_player]:
      if player == None:
        continue

      if player.robot == False:
        return player

    return None

  def start(self):
    '''
    kickstart the game by calling the ui display
    '''
    self.ui.display()

  def on_click(self, x, y):
    '''
    handle the click event
    '''

    player = self.get_human_player()
    if player == None:
      print 'no human player available. ui not clickable.'
      return

    print "click cell(%d,%d)" % (x, y)
    n = self.ncol*x + y

    # find the selected cell
    cell = self.canvass.get_cell((x,y))

    if player.move_status == 'idle':
      if player.is_self_piece((x,y)) == False:
        print 'Your can only select the pieces for yourself!'
        return

      # move to next select step
      player.move_status = 'selected'
      player.select_piece((x,y))
      player.add_cell_to_select_path((x,y))

      self.canvass.get_cell((x,y)).selected = True

    elif player.move_status == 'selected':
      x1, y1 = player.select_loc
      x2, y2 = x, y

      legal_move, terminated = self.is_legitimate_first_move((x1, y1), (x2, y2), player)
      if legal_move == False:
        print "This is not a legitimate move. Please re-consider!"
        return

      player.move_piece((x1, y1), (x2, y2))

      # move to next select step
      player.move_status = 'hopped'
      player.select_piece((x2,y2))
      player.add_cell_to_select_path((x2, y2))

      self.canvass.get_cell((x1,y1)).selected = False
      self.canvass.get_cell((x2,y2)).selected = True

      if terminated == True:
        player.move_status = 'stop'

    elif player.move_status == 'hopped':
      x1, y1 = player.select_loc
      x2, y2 = x, y

      # double click to end the selection
      if (x1, y1) == (x2, y2):
        player.move_status = 'idle'
        player.select_piece(None)
        player.clear_select_path()

        print 'end multi path selection'
        self.canvass.get_cell((x2,y2)).selected = False
      else:
        legal_move = self.is_legitimate_leap((x1, y1), (x2, y2), player)
        if legal_move == False:
          print "This is not a legitimate leap move. Please re-consider!"
          return

        player.move_piece((x1, y1), (x2, y2))

        # move to next select step
        player.move_status = 'hopped'
        player.select_piece((x2,y2))
        player.add_cell_to_select_path((x2, y2))

        self.canvass.get_cell((x1,y1)).selected = False
        self.canvass.get_cell((x2,y2)).selected = True
    elif player.move_status == 'stop':
      x1, y1 = player.select_loc
      x2, y2 = x, y

      # double click to end the selection
      if (x1, y1) == (x2, y2):
        player.move_status = 'idle'
        player.select_piece(None)
        player.clear_select_path()

        print 'end path selection'
        self.canvass.get_cell((x2,y2)).selected = False

    # print debug cell map
    self.canvass.print_debug_cell_map()
    
    # refresh the UI
    self.ui.refresh_playground()

    # only if the move finishes move to game ending check and fival play
    if player.move_status != 'idle':
      return

    # check the game ending condition after the move of the human player
    win_the_game, who = self.is_match_end()
    if win_the_game == True:
      self.ui.notify_win(who)
      print "%s wins the game!! Ending game!!!" % who

    #################################################
    # bot player engages
    #################################################
    rival = player.rival

    # get optimal move path
    # along with its move statistics
    move_path, move_stats = rival.whats_next_move()

    for loc in move_path:
      print "Moving path:" , loc

    nmove = len(move_path) - 1
    for i in range(nmove):
      loc_from = move_path[i]
      loc_to = move_path[i + 1]

      print "Moving path: %s -> %s" % (loc_from, loc_to)
      rival.move_piece(loc_from, loc_to)

      rival_leap, loc = self.is_leap_over_rival(loc_from, loc_to, rival)
      if rival_leap == True:
        player.remove_piece(loc)

      # refresh UI at each move with delay
      # FIXME (rw): this doesn't work, need more research
      #self.ui.refresh_playground()
      #time.sleep(0.5)

    self.ui.refresh_playground()

    # check the game ending condition after the move of the bot player
    win_the_game, who = self.is_match_end()
    if win_the_game == True:
      self.ui.notify_win(who)
      print "%s wins the game!! Ending game!!!" % who

    #################################################
    # bot player disengages
    #################################################

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

    if self.is_castle_occupied(self.north_player) or self.is_all_pieces_dead(self.north_player):
      # south wins the game
      # end the game with notification
      return True, "south"
    elif self.is_castle_occupied(self.south_player) or self.is_all_pieces_dead(self.south_player):
      # north wins the game
      # end the game with notification
      return True, "north"

    return False, None

  def is_castle_occupied(self, player):
    '''
    Check if the castle of any side is occupied
    This is one of the game winning(end) rules

    Input: side = "north" or "south"
    Output: True / False

    north castle points: (0, 3), (0, 4)
    south castle points: (13, 3), (13, 4)
    '''

    castle_points = player.castle_points
    rival = player.rival

    for x,y in castle_points:
      if rival.is_self_piece((x,y)):
        return True

    return False

  def is_all_pieces_dead(self, player):
    '''
    Check if all pieces of any side are dead
    This is one of the game winning(end) rules

    Input: player
    Output: True / False
    '''
    if player.list_of_pieces == []:
      return True
    else:
      return False

  def is_leap_over_rival(self, loc_start, loc_end, player):
    '''
    Check if (x1, y1) -> (x2, y2) is a leap over rival
    this is a helper function to determine whether one rival needs to be taken

    Return Value:
      status - True/False, whether it is a leap over rival
      loc    - (x,y) location of the rival
    '''

    x1, y1 = loc_start
    x2, y2 = loc_end

    x = (x1+x2)/2
    y = (y1+y2)/2
    cell = self.canvass.get_cell((x,y))
    if cell.status == player.rival.side:
      return True, (x,y)
    else:
      return False, None

  def is_legitimate_leap(self, loc_start, loc_end, player):
    '''
    This function checks whether a leap move is legal
    As leap move might involve removal of rival's cells
    player is required in order to identify its identity

    Input : loc_start is a tuple of (x,y)
            loc_end   is a tuple of (x,y)
            player    is the game player object
    Output: True/False
            True  - it is a legal move
                    if it's leaped on rival's cells, they are removed from the cell map
                    if it's leaped on its own cells, just leap
            False - it is not a legal move
    '''
    if loc_end in player.select_path:
      print 'loop move is not allowed'
      return False

    x1, y1 = loc_start
    x2, y2 = loc_end

    if (abs(x2-x1)!=0 and abs(x2-x1)!=2) or (abs(y2-y1)!=0 and abs(y2-y1)!=2):
      print 'too far away'
      return False

    x = (x1+x2)/2
    y = (y1+y2)/2
    cell = self.canvass.get_cell((x,y))
    print 'cell status: %s' % cell.status
    if cell.status == player.side:
      return True
    elif cell.status == player.rival.side:
      player.rival.remove_piece((x,y))
      return True
    else:
      return False

  def is_legitimate_first_move(self, loc_start, loc_end, player):
    '''
    This function checks whether the first jump is legitimate
    The reason to distinguish first jump is first jump could be either
    plain move or leap move while the successive moves could be only leap move

    Input: loc_start: (x,y) a tuple of row and column index
           loc_end  : (x,y) a tuple of row and column index
           player   : need to know the play in order to do leap move
                      because leap move might involve removal of rival's cells

    Return Value: whether_this_is_a_legal_move (True/False), whether_it_is_terminated_move
        A legitimate plain move is a True for first move
        A legitimate leap move is a True for first move
        terminated move means the first move is a plain move. In this case it is not allowed to move again
        If the first move is a leap move, it is ok to leap again and again.
    '''
    x1, y1 = loc_start
    x2, y2 = loc_end

    idx1 = x1*self.ncol + y1
    idx2 = x2*self.ncol + y2
    print "Trying to move from (%d, %d)[idx %d] to (%d, %d)[idx %d]" % \
        (x1, y1, idx1, x2, y2, idx2)

    # only free cell is movable target
    cell = self.canvass.get_cell((x2,y2))
    if cell.status != 'free':
      return False, True

    # Check plain move
    if max(abs(x2-x1),abs(y2-y1))==1:
      return True, True
    else:
      # check leap move
      is_legal_leap = self.is_legitimate_leap(loc_start, loc_end, player)
      return is_legal_leap, False


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
  player1 = Player(robot = False, name = 'bobcat', side = 'north')
  player2 = Player(robot = True,  name = 'caicai', side = 'south')

  game = GameEngine(player1, player2)

  # kick off the game with UI
  game.start()

#
# command line execution starts from here
#
if __name__ == '__main__':
  main(sys.argv[1:])

