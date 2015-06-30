#!/usr/bin/python

"""
Password Manager

Example:
 ./pwmgr -a -u <username> -p <password>
 ./pwmgr -c -u <username> -p <password>
 ./pwmgr -t [ECB,CTR,CBC]
"""

import os
import argparse

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('--user', default=None, help='username')
  parser.add_argument('--pass1', default=None, help='password')
  parser.add_argument('--add', help='add password into database')
  parser.add_argument('--check', help='check password validity')
  parser.add_argument('--type', default='ECB', help='cipher text type')

  ARGS = parser.parse_args()

  print ARGS.user, ARGS.pass1, ARGS.add

if __name__ == '__main__':
  main()

