#!/usr/bin/python
#
# playground.py

'''
 this is the playground canvass for the game
'''

#from Tkinter import *
from Tkinter import Tk, Canvas, Menu, Label, Button, PhotoImage, DISABLED, NORMAL


class PlayGround(object):
  '''
  play ground for the game canvass
  the button_map is made of 8 x 14 squared cells
  '''

  # pylint: disable=too-many-instance-attributes
  # we just need those attributes
  def __init__(self, game):

    self.unit = 50
    self.margin = 20

    self.gui = Tk()
    self.gui.title('caicai AI programming assignment')

    self.button_map = dict()

    ncol = game.ncol
    nrow = game.nrow

    self.width = self.margin * 2 + self.unit * ncol
    self.height = self.margin * 4 + self.unit * nrow
    self.game = game

    self.icon_white = PhotoImage(file="images/white.gif")
    self.icon_black = PhotoImage(file="images/black.gif")
    self.icon_none = PhotoImage(file="images/none.gif")

    self.prepare_the_playground(ncol, nrow)

    # end game label with a gif photo
    self.photo_endgame = PhotoImage(file="images/game-over.gif")
    self.label_endgame = Label(image=self.photo_endgame)
    self.label_endgame.image = self.photo_endgame

  def display(self):
    '''
    start the display mainloop
    All buttons will be on the screen right now
    '''
    self.gui.mainloop()

  def make_menu(self):
    '''
    make the menu bar
    '''
    menubar = Menu(self.gui)

    menubar.add_command(label='Reset Game', command=self.game.reset_game)
    menubar.add_command(label='About', command=self.game.about_me)

    self.gui.config(menu=menubar)

  def prepare_the_playground(self, ncol, nrow):
    '''
    draw the playground according to the cell status map
    different status maps to different color
    '''

    # place the canvas
    canvass = Canvas(self.gui, bg="white", height=self.height, width=self.width)
    canvass.pack()

    # place the menu
    self.make_menu()

    # place the buttons
    for row_idx in range(nrow):
      for col_idx in range(ncol):
        idx = ncol * row_idx + col_idx

        cell = self.game.canvass.get_cell((row_idx, col_idx))

        # active buttons, with callback function passing the button index
        if cell.status == 'disabled':
          # disabled buttons, which are unclickable
          button = Button(self.gui,
                          state=DISABLED,
                          height=50,
                          width=50,
                          background='#875b00')
        elif cell.status == 'free':
          color = 'white'
          button = Button(self.gui, activebackground=color, height=50, width=50, cursor="target", \
              background='#dbb25c', \
              command=lambda row_idx=row_idx, col_idx=col_idx: self.game.on_click(row_idx, col_idx))
        elif cell.status == 'north':
          button = Button(self.gui, activebackground='grey', height=50, width=50, cursor="target", \
              image=self.icon_white, background='#dbb25c', \
              command=lambda row_idx=row_idx, col_idx=col_idx: self.game.on_click(row_idx, col_idx))
        elif cell.status == 'south':
          button = Button(self.gui, activebackground='grey', height=50, width=50, cursor="target", \
              image=self.icon_black, background='#dbb25c', \
              command=lambda row_idx=row_idx, col_idx=col_idx: self.game.on_click(row_idx, col_idx))

        # calculate the x,y coordinates and place the buttons
        offset_x = self.margin + self.unit * col_idx
        offset_y = 3 * self.margin + self.unit * row_idx
        button.place(x=offset_x, y=offset_y, width=self.unit, height=self.unit)

        self.button_map[idx] = button

  def refresh_playground(self):
    '''
    refresh the playground
    '''

    print "refreshing ui according to the cell status map"

    nrow = self.game.nrow
    ncol = self.game.ncol

    for row_idx in range(nrow):
      for col_idx in range(ncol):
        cell = self.game.canvass.get_cell((row_idx, col_idx))
        idx = ncol * row_idx + col_idx
        button = self.button_map[idx]

        if cell.lock == True:
          button.configure(state=DISABLED)
          continue
        else:
          button.configure(state=NORMAL)

        if cell.status == 'free':
          button.configure(image=self.icon_none)
        elif cell.status == 'north':
          button.configure(image=self.icon_white)
        elif cell.status == 'south':
          button.configure(image=self.icon_black)

        if cell.selected == True:
          button.configure(bg="#234")
        else:
          if cell.status == 'disabled':
            button.configure(bg="#875b00")
          else:
            button.configure(bg="#dbb25c")

  def reset_ui(self):
    '''
    reset UI by hiding the game winning picture from the canvass
    '''
    self.label_endgame.place_forget()

  def notify_win(self, who):
    '''
    notify the game ending by annoucing the winner on top
    the whole canvass will be locked and unclickable at this point
    '''

    if who == 'north' or who == 'south':
      self.game.canvass.lock_canvass()
      self.refresh_playground()
      self.label_endgame.place(x=20, y=260)

