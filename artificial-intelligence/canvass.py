#!/usr/bin/python
#
# playground.py
#
# this is the playground canvass for the game
#

from pprint import pprint
from Tkinter import *

class Cell():
  '''
  one cell of the game canvass
  '''
  x = 0
  y = 0
  status = 'disabled'

  def __init__(self, x, y, status):
    self.x = x
    self.y = y
    self.status = status

  def set_xy(self, x, y):
    self.x = x
    self.y = y

  def set_status(self, status):
    self.status = status


class PlayGround():
  '''
  play ground for the game canvass
  the canvass is made of 8 x 14 squared cells
  '''

  width = 0
  height = 0
  unit = 50
  margin = 20

  player = None

  canvass = dict()

  def __init__(self, player, ncol = 8, nrow = 14):

    self.width = self.margin * 2 + self.unit * ncol
    self.height = self.margin * 4 + self.unit * nrow
    self.player = player

    self.init_cells(ncol, nrow)

    self.draw_the_playground(ncol, nrow)

  def init_cells(self, ncol, nrow):
    '''
    initialize cell coordinates and state

    'free'       - the cell is not used
    'disabled'   - the cell is disabled
    'play_bot'   - the cell is occupied by the AI robot
    'play_human' - the cell is occupied by the human player
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

  def draw_the_playground(self, ncol, nrow):

    top = Tk()
    top.title('caicai AI programming assignment')

    w = Canvas(top, bg="white", height = self.height, width = self.width)
    w.pack()

    for i in range(nrow):
      for j in range(ncol):
        n = ncol*i + j

        cell = self.canvass[n]['cell']

        if cell.status == 'disabled':
          color = 'grey'
        elif cell.status == 'free':
          color = 'white'
        elif cell.status == 'play_bot':
          color = 'blue'
        elif cell.status == 'play_human':
          color = 'purple'

        if color == 'grey':
          button = Button(top, state = DISABLED, height = 50, width = 50)
        else:
          button = Button(top, activebackground = 'white', height = 50, width = 50, cursor = "target", background = color, command = self.player.on_click(cell))

        x = self.margin + self.unit * j
        y = 3 * self.margin + self.unit * i
        button.place(x=x, y=y, width=self.unit, height=self.unit)

        self.canvass[n]['button'] = button

    top.mainloop()

  def refresh_playground(self):
    pass

