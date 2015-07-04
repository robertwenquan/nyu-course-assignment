#!/usr/bin/python

"""
Password Manager

Homework assignment for Application Security
Summer 2015
Polychenic School of Engineer, NYU

Robert Wen <robert.wen@nyu.edu>
NetID: qw476
N12246277

Example:
 ./pwmgr -a -u <username> -p <password>
 ./pwmgr -c -u <username> -p <password>
 ./pwmgr -t [ECB,CTR,CBC]
"""

import os
import sys
import argparse

class PasswordStore():
  '''
  '''

class PasswordManager():
  '''
  class for global password manager
  '''

  ARGS = None

  def __init__(self, argv):
    self.ARGS = self.init_args(argv)

  def init_args(self, argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('--user', default=None, help='username')
    parser.add_argument('--pass', default=None, help='password')
    parser.add_argument('-a', nargs='?', help='add password into database')
    parser.add_argument('-c', nargs='?', help='check password validity')
    parser.add_argument('--type', default='ECB', help='cipher text type')

    ARGS = parser.parse_args(argv)
    return ARGS

class Password():
  '''
  class for password entry
  '''

  username = None
  password = None
  passwd_cipher = None
  

def main():

  manager = PasswordManager(sys.argv[1:])
  print manager.ARGS.user
  print manager.ARGS.type

if __name__ == '__main__':
  main()

