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
    self.ui.title('caicai AI programming assignment')

    ncol = game.ncol
    nrow = game.nrow

    self.width = self.margin * 2 + self.unit * ncol
    self.height = self.margin * 4 + self.unit * nrow
    self.game = game

    self.icon_white = PhotoImage(file="images/white.gif")
    self.icon_black = PhotoImage(file="images/black.gif")
    self.icon_none = PhotoImage(file="images/none.gif")

    self.prepare_the_playground(ncol, nrow)

  def display(self):
    '''
    start the display mainloop
    All buttons will be on the screen right now
    '''
    self.ui.mainloop()

  def make_menu(self):
    menubar = Menu(self.ui)

    menubar.add_command(label = 'Reset Game', command = self.game.reset_game)
    menubar.add_command(label = 'About', command = self.game.about_me)

    self.ui.config(menu=menubar)

  def prepare_the_playground(self, ncol, nrow):
    '''
    draw the playground according to the cell status map
    different status maps to different color
    '''

    # place the canvas
    w = Canvas(self.ui, bg="white", height = self.height, width = self.width)
    w.pack()

    # place the menu 
    self.make_menu()

    # place the buttons
    for i in range(nrow):
      for j in range(ncol):
        n = ncol*i + j

        cell = self.game.canvass.get_cell((i,j))

        # active buttons, with callback function passing the button index
        if cell.status == 'disabled':
          # disabled buttons, which are unclickable
          button = Button(self.ui, state = DISABLED, height = 50, width = 50)
        elif cell.status == 'free':
          color = 'grey'
          button = Button(self.ui, activebackground = color, height = 50, width = 50, cursor = "target", \
              background = color, command = lambda x = i, y = j: self.game.on_click(x, y))
        elif cell.status == 'north':
          button = Button(self.ui, height = 50, width = 50, cursor = "target", image = self.icon_white, \
              background = 'grey', command = lambda x = i, y = j: self.game.on_click(x, y))
        elif cell.status == 'south':
          button = Button(self.ui, height = 50, width = 50, cursor = "target", image = self.icon_black, \
              background = 'grey', command = lambda x = i, y = j: self.game.on_click(x, y))

        # calculate the x,y coordinates and place the buttons
        x = self.margin + self.unit * j
        y = 3 * self.margin + self.unit * i
        button.place(x=x, y=y, width=self.unit, height=self.unit)

        self.button_map[n] = button

  def helloCallBack(self):
    print 'sdfsdfsdf'

  def refresh_playground(self):
    '''
    refresh the playground
    '''

    print "refreshing ui according to the cell status map"

    nrow = self.game.nrow
    ncol = self.game.ncol

    for i in range(nrow):
      for j in range(ncol):
        n = ncol*i + j
        cell = self.game.canvass.get_cell((i,j))
        button = self.button_map[n]

        if cell.status == 'free':
          button.configure(image = self.icon_none)
        elif cell.status == 'north':
          button.configure(image = self.icon_white)
        elif cell.status == 'south':
          button.configure(image = self.icon_black)
        else:
          pass

        if cell.selected == True:
          button.configure(bg = "#234")
        else:
          button.configure(bg = "grey")
