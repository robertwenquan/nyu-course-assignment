#!/usr/bin/python

"""
 this is the Mini Camelot game
 for CS-GY 6613 Artificial Intelligence course in Spring 2015 semester

 this source code defines the GUI part of the game.
 The GUI is based on Python Tkinter interface via Tcl/Tk
"""

__author__ = "Caicai CHEN <caicai.chen@nyu.edu>"
__date__ = "22 Apr 2015"

from Tkinter import Tk, Canvas, Menu
from Tkinter import Label, Button, Radiobutton
from Tkinter import PhotoImage, Toplevel
from Tkinter import DISABLED, NORMAL, FALSE
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

    self.button_map = dict()

    ncol = game.ncol
    nrow = game.nrow

    self.choose_side = 'north'
    self.choose_level = 2

    self.width = self.margin * 2 + self.unit * ncol
    self.height = self.margin * 5 + self.unit * nrow
    self.game = game

    # main window
    self.gui = Tk()
    self.gui.title('Mini Camelot')
    self.gui.resizable(width=FALSE, height=FALSE)

    # icons
    self.icon_white = PhotoImage(file="images/white.gif")
    self.icon_black = PhotoImage(file="images/black.gif")
    self.icon_none = PhotoImage(file="images/none.gif")
    self.icon_disabled = PhotoImage(file="images/disabled.gif")

    self.prepare_the_playground(ncol, nrow)

    # end game label with a gif photo
    self.photo_endgame_win = PhotoImage(file="images/game-over-win.gif")
    self.label_endgame_win = Label(image=self.photo_endgame_win)
    self.label_endgame_win.image = self.photo_endgame_win

    self.photo_endgame_lose = PhotoImage(file="images/game-over-lose.gif")
    self.label_endgame_lose = Label(image=self.photo_endgame_lose)
    self.label_endgame_lose.image = self.photo_endgame_lose

    self.photo_endgame_north_win = PhotoImage(file="images/game-over-north-win.gif")
    self.label_endgame_north_win = Label(image=self.photo_endgame_north_win)
    self.label_endgame_north_win.image = self.photo_endgame_north_win

    self.photo_endgame_south_win = PhotoImage(file="images/game-over-south-win.gif")
    self.label_endgame_south_win = Label(image=self.photo_endgame_south_win)
    self.label_endgame_south_win.image = self.photo_endgame_south_win

    # game options pop up box
    self.select_start_options()

    # FINISH initialization, READY to start the game

  def display(self):
    '''
    start the display mainloop
    All buttons will be on the screen right now
    '''
    self.gui.mainloop()

  def make_top_bar(self):
    '''
    make the top bar, with game restart, and statistics information
    '''

    # reset game button
    button = Button(self.gui, text='reset game', height=30, width=120, \
                    command=self.reset_game)
    button.place(x=20, y=20, width=120, height=20)

    # about me button
    button = Button(self.gui, text='about me', height=30, width=120, \
                    command=self.about_me)
    button.place(x=160, y=20, width=120, height=20)

    # four labels for statistical numbers
    self.label_max_depth = Label(self.gui, text='0')
    self.label_nodes = Label(self.gui, text='0')
    self.label_prune_max = Label(self.gui, text='0')
    self.label_prune_min = Label(self.gui, text='0')

    self.label_max_depth.place(x=20, y=50, width=70, height=20)
    self.label_nodes.place(x=100, y=50, width=70, height=20)
    self.label_prune_max.place(x=180, y=50, width=70, height=20)
    self.label_prune_min.place(x=260, y=50, width=70, height=20)

  def reset_game(self):
    '''
    restart game by re-selecting game options (side and level)
    '''
    self.game.reset_game()
    self.clear_statistics()
    self.select_start_options()

  def about_me(self):
    '''
    show the author and version of this application
    '''
    print 'about me'

  def select_start_options(self):
    '''
    popup box to select side and difficulty levels
    '''
    print 'select game start options'

    popup = Toplevel(self.gui, width=300, height=110)
    popup.title('Choose Game Side and Level')

    # stays on top of the game canvass
    popup.transient(self.gui)
    popup.grab_set()

    # bind window close events
    popup.bind('<Escape>', lambda e: self.not_selected_start_options(popup))
    popup.protocol("WM_DELETE_WINDOW", lambda : self.not_selected_start_options(popup))

    # choose side
    label1 = Label(popup, text="Side", height=30, width=50)
    label1.place(x=10, y=5, height=30, width=50)

    val1 = IntVar()

    bt_north = Radiobutton(popup, text="White", variable=val1, value=1)
    bt_north.place(x=60, y=10)
    bt_south = Radiobutton(popup, text="Black", variable=val1, value=2)
    bt_south.place(x=120, y=10)

    # by default, human plays first, meaning play the north side
    if self.choose_side == 'north':
      bt_north.select()
    else:
      bt_south.select()

    # choose difficulty level
    label2 = Label(popup, text="Level", height=30, width=50)
    label2.place(x=10, y=35, height=30, width=50)

    val2 = IntVar()

    bt_level1 = Radiobutton(popup, text="Dumb", variable=val2, value=1)
    bt_level1.place(x=60, y=40)
    bt_level2 = Radiobutton(popup, text="Smart", variable=val2, value=2)
    bt_level2.place(x=120, y=40)
    bt_level3 = Radiobutton(popup, text="Genius", variable=val2, value=3)
    bt_level3.place(x=180, y=40)

    # by default, the game is medium level
    if self.choose_level == 1:
      bt_level1.select()
    elif self.choose_level == 2:
      bt_level2.select()
    elif self.choose_level == 3:
      bt_level3.select()

    button = Button(popup, text='SET', \
              command=lambda: self.selected_start_options(popup, val1, val2))

    button.place(x=70, y=70)

  def not_selected_start_options(self, popup):
    '''
    actions for closing the game option window
    '''

    self.game.start_game()

    popup.grab_release()
    popup.destroy()

  def selected_start_options(self, popup, choose_side, choose_level):
    '''
    this is the callback function of the submit button
    for the game start options
    '''

    side_name = {1 : 'north',
                 2 : 'south'}

    self.choose_side = side_name[choose_side.get()]
    self.choose_level = int(choose_level.get())

    print 'Selected start options'
    print 'Side', self.choose_side
    print 'Level', self.choose_level

    self.game.start_game()

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
          button = Button(self.gui, state=DISABLED)
        else:
          button = Button(self.gui, cursor="target", \
                          command=lambda row_idx=row_idx, col_idx=col_idx: \
                                         self.game.human_play(row_idx, col_idx))

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

        if cell.status == 'free':
          button.configure(image=self.icon_none)
        elif cell.status == 'north':
          button.configure(image=self.icon_white)
        elif cell.status == 'south':
          button.configure(image=self.icon_black)
        elif cell.status == 'disabled':
          button.configure(image=self.icon_disabled)

        if cell.selected == True:
          button.configure(bg="#234")
        else:
          if cell.status == 'disabled':
            button.configure(bg="#875b00")
          else:
            button.configure(bg="#dbb25c")

        if cell.lock == True:
          button.configure(state=DISABLED)
        else:
          button.configure(state=NORMAL)

  def reset_ui(self):
    '''
    reset UI by hiding the game winning picture from the canvass
    '''
    self.label_endgame_win.place_forget()
    self.label_endgame_lose.place_forget()
    self.label_endgame_north_win.place_forget()
    self.label_endgame_south_win.place_forget()

  def notify_win(self, who):
    '''
    notify the game ending by annoucing the winner on top
    the whole canvass will be locked and unclickable at this point
    '''

    assert who == 'north' or who == 'south'

    # robot only mode
    if self.game.robot_mode == True:
      if who == 'north':
        #self.label_endgame_north_win.place(x=20, y=219)
        pass
      else:
        #self.label_endgame_south_win.place(x=20, y=219)
        pass
      return

    # human engage mode
    self.game.canvass.lock_canvass()
    self.refresh_playground()

    player = self.game.get_human_player()
    assert player != None

    if player.side == who:
      self.label_endgame_win.place(x=20, y=219)
    else:
      self.label_endgame_lose.place(x=20, y=219)

  def clear_statistics(self):
    '''
    clear all statistics numbers to 0
    '''
    stats = (0, 0, 0, 0)
    self.update_statistics(stats)

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

    self.label_max_depth.config(text=str(max_depth_reached))
    self.label_nodes.config(text=str(nodes_generated))
    self.label_prune_max.config(text=str(num_pruning_max_value))
    self.label_prune_min.config(text=str(num_pruning_min_value))

