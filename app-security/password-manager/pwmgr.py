#!/usr/bin/env python

"""
Password Manager

Homework assignment for Application Security
Summer 2015
Polychenic School of Engineering, New York University

Robert Wen <robert.wen@nyu.edu>
NetID: qw476
N12246277

Installation:
 $ pip install -r requirements.txt

Example:
 ./pwmgr.py -a -u <username> -p <password> -t [ECB,CTR,CBC]
 ./pwmgr.py -c -u <username> -p <password> -t [ECB,CTR,CBC]
"""

import os
import sys
import string
import passlib
import argparse


class Logger():
  '''
  unified logger
  '''
  
  ENABLE_DEBUG = False

  def log(self, loglevel, log_string):
    if loglevel.upper() == 'DEBUG' and self.ENABLE_DEBUG == True:
      print log_string


class PasswordStore():
  '''
  '''

class PasswordManager():
  '''
  class for global password manager
  '''

  ARGS = None
  command_type = ''

  def __init__(self, argv):
    self.ARGS = self.init_args(argv)

  def init_args(self, argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', action='store_true', help='add password into database')
    parser.add_argument('-c', '--check', action='store_true', help='check password validity')
    parser.add_argument('-u', '--user', default=None, help='username')
    parser.add_argument('-p', '--passwd', default=None, help='password')
    parser.add_argument('-e', '--enc', default='ECB', help='cipher text encryption method')
    parser.add_argument('-d', '--debug', action='store_true', help='enable debugging output')

    ARGS = parser.parse_args(argv)

    # set logger DEBUG flag
    if ARGS.debug:
      logger.ENABLE_DEBUG = True

    # print arguments
    logger.log('DEBUG', 'argument check: --add %s' % ARGS.add)
    logger.log('DEBUG', 'argument check: --check %s' % ARGS.check)
    logger.log('DEBUG', 'argument check: --user %s' % ARGS.user)
    logger.log('DEBUG', 'argument check: --passwd %s' % ARGS.passwd)

    check_status = self.check_args(ARGS)
    if not check_status:
      parser.print_help()
      exit(2)

    return ARGS

  def check_args(self, args):

    # check command type
    arg_add = args.add
    arg_chk = args.check

    if not arg_add and not arg_chk:
      # must choose one command type
      return False

    if arg_add and not arg_chk:
      self.command_type = 'add'
    elif not arg_add and arg_chk:
      self.command_type = 'check'
    else:
      # only one command type could be selected
      return False

    # check user and pass
    arg_user = args.user
    arg_pass = args.passwd

    if not arg_user or not arg_pass:
      # username and password must be valid
      return False

    # check encryption type
    arg_enc_type = args.enc
    if arg_enc_type.upper() != 'ECB' and arg_enc_type.upper() != 'CTR' \
      and arg_enc_type.upper() != 'CBC':
      return False

    return True

  def add_passwd(self):

    user = self.ARGS.user

    '''
    if self.user_exists(user):
      throw error
      return

    passwd_plain = self.ARGS.passwd
    passwd_enc_method = self.ARGS.enc

    passwd_cipher = self.encrypt_passwd(passwd_plain, self.random_string(), passwd_enc_method)

    self.user_add(user, passwd_cipher, passwd_enc_method)

    print 'user created'

    '''

    print 'add passwd finished'

  def check_passwd(self):

    user = self.ARGS.user

    '''
    if not self.user_exists(user):
      throw error
      return

    passwd_plain = self.ARGS.passwd
    passwd_enc_method = self.ARGS.enc

    passwd_cipher = self.encrypt_passwd(passwd_plain, self.random_string(), passwd_enc_method)

    if self.user_verify(user, passwd_cipher, passwd_enc_method):
      good
    else:
      bad
    
    '''

    print 'check passwd finished'

  @classmethod
  def random_string(cls, length=16):
    char_samples = string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_str = ''.join(random.choice(char_samples) for _ in range(length))
    return random_str

  def encrypt_passwd(self, plaintext, salt, enc_type='ECB'):
    if enc_type != 'ECB' and enc_type != 'CTR' and enc_type != 'CBC':
      return None

    if enc_type == 'ECB':
      cipher = passlib.hash.sha512_crypt.encrypt(plaintext, salt=salt, rounds=5000)

    return cipher


class Password():
  '''
  class for password entry
  '''

  username = None
  password = None
  passwd_cipher = None
  

def main():

  manager = PasswordManager(sys.argv[1:])

  if manager.command_type == 'add':
    manager.add_passwd()
  elif manager.command_type == 'check':
    manager.check_passwd()
  else:
    raise ValueError('Unsupported command type')

if __name__ == '__main__':
  logger = Logger()
  main()

