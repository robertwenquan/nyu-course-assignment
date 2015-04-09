#!/usr/bin/python
#
# playground.py
#
# this is the playground canvass for the game
#

from pprint import pprint
from Tkinter import *
import tkMessageBox

class Cell():
  '''
  one cell of the game canvass
  '''
  x = 0
  y = 0
  status = 'disabled'

  def init(self, x, y, status):
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

  def __init__(self, ncol = 8, nrow = 14):
    self.width = self.margin * 2 + self.unit * ncol
    self.height = self.margin * 2 + self.unit * nrow

    self.draw_the_playground(ncol, nrow)

  def draw_the_playground(self, ncol, nrow):

    top = Tk()

    w = Canvas(top, bg="white", height = self.height, width = self.width)
    w.pack()

    icon=PhotoImage(file="box.gif")
    Buttons = dict()

    for i in range(ncol):
      for j in range(nrow):
        n = 10*i + j

        Buttons[n] = Button(top, activebackground = 'white', height = 50, width = 50, image = icon, text = str(n), command = helloCallBack)
        x = 20 + 50 * i
        y = 20 + 50 * j
        Buttons[n].place(x=x, y=y)

    top.mainloop()


def helloCallBack():
  tkMessageBox.showinfo( "Hello Python", "Hello World")

PG = PlayGround()

