#!/usr/bin/python
#
# playground.py
#
# this is the playground canvass for the game
#

from Tkinter import *

class PlayGround():
  '''
  play ground for the game canvass
  the button_map is made of 8 x 14 squared cells
  '''

  width = 0
  height = 0
  unit = 50
  margin = 20

  ui = None
  button_map = dict()

  def __init__(self, game):

    self.ui = Tk()

    ncol = game.ncol
    nrow = game.nrow

    self.width = self.margin * 2 + self.unit * ncol
    self.height = self.margin * 4 + self.unit * nrow
    self.game = game

    self.prepare_the_playground(ncol, nrow)

  def display(self):
    self.ui.mainloop()

  def prepare_the_playground(self, ncol, nrow):
    '''
    draw the playground according to the cell status map
    different status maps to different color
    '''

    self.ui.title('caicai AI programming assignment')

    w = Canvas(self.ui, bg="white", height = self.height, width = self.width)
    w.pack()

    for i in range(nrow):
      for j in range(ncol):
        n = ncol*i + j

        cell = self.game.canvass[n]['cell']

        if cell.status == 'disabled':
          color = 'black'
        elif cell.status == 'free':
          color = 'grey'
        elif cell.status == 'play_bot':
          color = 'blue'
        elif cell.status == 'play_human':
          color = 'purple'

        if color == 'black':
          # disabled buttons, which are unclickable
          button = Button(self.ui, state = DISABLED, height = 50, width = 50)
        else:
          # active buttons, with callback function passing the button index
          button = Button(self.ui, activebackground = 'white', height = 50, width = 50, cursor = "target", background = color, command = lambda x = i, y = j: self.game.on_click(x, y))

        # calculate the x,y coordinates and place the buttons
        x = self.margin + self.unit * j
        y = 3 * self.margin + self.unit * i
        button.place(x=x, y=y, width=self.unit, height=self.unit)

        self.button_map[n] = {'button' : button}

  def refresh_playground(self):
    '''
    refresh the playground
    '''
    print "refreshing ui according to the cell status map"
    #button.configure(bg = "#234")
    pass

