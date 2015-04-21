#!/usr/bin/python

"""
 this is the Mini Camelot game
 for CS-GY 6613 Artificial Intelligence course in Spring 2015 semester

 this source code defines the GUI part of the game.
 The GUI is based on Python Tkinter interface via Tcl/Tk
"""

from Tkinter import Tk, Canvas, Menu
from Tkinter import Label, Button, Radiobutton
from Tkinter import PhotoImage, Toplevel
from Tkinter import DISABLED, NORMAL, LEFT
from Tkinter import IntVar


class PlayGround(object):
  '''
  play ground for the game canvass
  the button_map is made of 8 x 14 squared cells
  '''

  # pylint: disable=too-many-instance-attributes
  # we just need those attributes
  def __init__(self, game):

    self.unit = 40
    self.margin = 20

    self.gui = Tk()
    self.gui.title('Mini Camelot')

    self.button_map = dict()

    ncol = game.ncol
    nrow = game.nrow

    self.width = self.margin * 2 + self.unit * ncol
    self.height = self.margin * 5 + self.unit * nrow
    self.game = game

    self.icon_white = PhotoImage(file="images/white.gif")
    self.icon_black = PhotoImage(file="images/black.gif")
    self.icon_none = PhotoImage(file="images/none.gif")

    self.prepare_the_playground(ncol, nrow)

    # end game label with a gif photo
    self.photo_endgame = PhotoImage(file="images/game-over.gif")
    self.label_endgame = Label(image=self.photo_endgame)
    self.label_endgame.image = self.photo_endgame

    # game options pop up box
    self.select_start_options()

    # FINISH initialization, READY to start the game

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

    menubar.add_command(label='About', command=self.game.about_me)

    self.gui.config(menu=menubar)

  def make_top_bar(self):
    '''
    make the top bar, with game restart, and statistics information
    '''

    # start game button
    button = Button(self.gui, text = 'start game', height=30, width=120, \
                    command=self.game.start_game)
    button.place(x=20, y=20, width=120, height=20)

    # reset game button
    button = Button(self.gui, text = 'reset game', height=30, width=120, \
                    command=self.game.reset_game)
    button.place(x=160, y=20, width=120, height=20)

    self.label_max_depth = Label(self.gui, text = '0')
    self.label_nodes = Label(self.gui, text = '0')
    self.label_prune_max = Label(self.gui, text = '0')
    self.label_prune_min = Label(self.gui, text = '0')

    self.label_max_depth.place(x=20, y=50, width=70, height=20)
    self.label_nodes.place(x=100, y=50, width=70, height=20)
    self.label_prune_max.place(x=180, y=50, width=70, height=20)
    self.label_prune_min.place(x=260, y=50, width=70, height=20)

  def about_me(self):
    '''
    show the author and version of this application
    '''
    pass

  def select_start_options(self):
    '''
    popup box to select side and difficulty levels
    '''
    print 'select game start options'

    popup = Toplevel(self.gui, width=300, height=110)
    popup.grab_set()

    # choose side 
    label1 = Label(popup, text="Side", height=30, width=50)
    label1.place(x=10, y=5, height=30, width=50)

    v1 = IntVar()

    bt_north = Radiobutton(popup, text="White", variable=v1, value=1)
    bt_north.place(x=60,y=10)
    bt_south = Radiobutton(popup, text="Black", variable=v1, value=2)
    bt_south.place(x=120, y=10)

    # by default, human plays first, meaning play the north side
    bt_north.select()

    # choose difficulty level
    label2 = Label(popup, text="Level", height=30, width=50)
    label2.place(x=10, y=35, height=30, width=50)

    v2 = IntVar()

    bt_level1 = Radiobutton(popup, text="Dumb", variable=v2, value=1)
    bt_level1.place(x=60, y=40)
    bt_level2 = Radiobutton(popup, text="Smart", variable=v2, value=2)
    bt_level2.place(x=120, y=40)
    bt_level3 = Radiobutton(popup, text="Genius", variable=v2, value=3)
    bt_level3.place(x=180, y=40)

    # by default, the game is hard
    bt_level3.select()

    button = Button(popup, text='SET', \
              command=lambda: self.selected_start_options(popup, v1, v2))

    button.place(x=70, y=70)

  def selected_start_options(self, popup, choose_side, choose_level):
    '''
    this is the callback function of the submit button
    for the game start options
    '''

    SIDE = { 1 : 'north' ,
             2 : 'south'
           }

    LEVEL = { 1 : 'tao2' ,
              2 : 'tao1' ,
              3 : 'caicai'
            }

    self.choose_side = SIDE[choose_side.get()]
    self.choose_level = LEVEL[choose_level.get()]

    print 'selected start options'
    print 'Side', self.choose_side
    print 'Level', self.choose_level

    popup.grab_release()
    popup.destroy()

  def prepare_the_playground(self, ncol, nrow):
    '''
    draw the playground according to the cell status map
    different status maps to different color
    '''

    # place the canvas
    canvass = Canvas(self.gui, bg="white", height=self.height, width=self.width)
    canvass.pack()

    # place top bar
    self.make_top_bar()

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
              command=lambda row_idx=row_idx, col_idx=col_idx: self.game.human_play(row_idx, col_idx))
        elif cell.status == 'north':
          button = Button(self.gui, activebackground='grey', height=50, width=50, cursor="target", \
              image=self.icon_white, background='#dbb25c', \
              command=lambda row_idx=row_idx, col_idx=col_idx: self.game.human_play(row_idx, col_idx))
        elif cell.status == 'south':
          button = Button(self.gui, activebackground='grey', height=50, width=50, cursor="target", \
              image=self.icon_black, background='#dbb25c', \
              command=lambda row_idx=row_idx, col_idx=col_idx: self.game.human_play(row_idx, col_idx))

        # calculate the x,y coordinates and place the buttons
        offset_x = self.margin + self.unit * col_idx
        offset_y = 4 * self.margin + self.unit * row_idx
        button.place(x=offset_x, y=offset_y, width=self.unit, height=self.unit)

        self.button_map[idx] = button

    self.refresh_playground()

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
      self.label_endgame.place(x=20, y=219)

  def update_statistics(self, move_stats):
    '''
    update the move statistics for the bot player, for each move

    Four metrics are collected for the statistics:
     - max_depth_reached
     - nodes_generated-
     - num_pruning_max_value
     - num_pruning_min_value
    '''

    max_depth_reached, nodes_generated, \
    num_pruning_max_value, num_pruning_min_value = move_stats

    print 'updating moving statistics...'

    self.label_max_depth.config(text = str(max_depth_reached))
    self.label_nodes.config(text = str(nodes_generated))
    self.label_prune_max.config(text = str(num_pruning_max_value))
    self.label_prune_min.config(text = str(num_pruning_min_value))

