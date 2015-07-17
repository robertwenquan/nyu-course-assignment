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
 ./pwmgr.py -a -u <username> -p <password> -e [ECB,CTR,CBC]
 ./pwmgr.py -c -u <username> -p <password> -e [ECB,CTR,CBC]
 ./pwmgr.py -l
"""

import os
import sys
import random
import string
from passlib.hash import sha512_crypt
from Crypto.Cipher import AES
import argparse
import sqlite3


MASTER_KEY_FILE = '~/.pwmgr.key'

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
  password store, backed by sqlite
  '''

  def __init__(self):
    self.connection = sqlite3.connect('passwd_manager.db')
    self.connection.isolation_level = None

  def user_exists(self, username):
    ''' check if the username exists in the database '''

    cur = self.connection.cursor()
    sql_statmt = "SELECT * from shadow WHERE username = '%s'" % username
    cur.execute(sql_statmt)
    if cur.fetchone():
      return True
    else:
      return False

  def user_add(self, username, password):
    ''' add a hashed password entry '''
    cur = self.connection.cursor()
    sql_statmt = "INSERT into shadow VALUES('%s', '%s')" % (username, password)
    cur.execute(sql_statmt)
    # check error with the execution

  def user_verify(self, username, password):
    ''' verify username and hashed password from the database '''
    cur = self.connection.cursor()
    sql_statmt = "SELECT passwd FROM shadow WHERE username = '%s'" % username
    cur.execute(sql_statmt)

    one_rec = cur.fetchone()
    if not one_rec:
      return False

    # check error with the execution

    # get the salt
    # get the crypted one
    cipher_fetched = one_rec[0]
    _, enc_method, salt_key, encrypted_key = cipher_fetched.split('$')

    # recalculate the crypted one
    cipher_recalculated = sha512_crypt.encrypt(password, salt=salt_key, rounds=5000)

    logger.log('DEBUG', 'username: %s' % username)
    logger.log('DEBUG', 'password: %s' % password)
    logger.log('DEBUG', 'salt: %s' % salt_key)
    logger.log('DEBUG', 'hashed0: %s' % encrypted_key)
    logger.log('DEBUG', 'hashed1: %s' % cipher_recalculated)

    # compare them
    if cipher_recalculated == cipher_fetched:
      return True
    else:
      return False

    # distinguish user-not-exist and password-error
  
  def list_users(self):
    ''' list all users from the databases '''

    cur = self.connection.cursor()
    sql_statmt = "SELECT username, passwd FROM shadow"
    cur.execute(sql_statmt)

    for (user, passwd) in cur.fetchall():
      enc = passwd.split('$')[1]
      salt = passwd.split('$')[2]
      encrypted = passwd.split('$')[3]
      print "%10s %16s %s" % (user, salt, encrypted)


class PasswordManager():
  '''
  class for global password manager
  '''

  ARGS = None
  command_type = ''
  masterkey = ''

  def __init__(self, argv):
    self.ARGS = self.init_args(argv)
    self.password_store = PasswordStore()
    self.masterkey = self.init_masterkey()

  def init_args(self, argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', action='store_true', help='add password into database')
    parser.add_argument('-c', '--check', action='store_true', help='check password validity')
    parser.add_argument('-l', '--list', action='store_true', help='list users from the password database')
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
    logger.log('DEBUG', 'argument check: --list %s' % ARGS.list)
    logger.log('DEBUG', 'argument check: --user %s' % ARGS.user)
    logger.log('DEBUG', 'argument check: --passwd %s' % ARGS.passwd)

    check_status = self.check_args(ARGS)
    if not check_status:
      parser.print_help()
      exit(2)

    return ARGS

  def init_masterkey(self):
    ''' init masterkey '''

    writeback = False

    try:
      filename = os.path.expanduser(MASTER_KEY_FILE)
      masterkey = open(filename).read()
    except:
      masterkey = self.random_string(64)
      writeback = True

    if writeback:
      try:
        open(filename, 'w').write(masterkey)
      except:
        return None

    return masterkey

  def check_args(self, args):

    # check command type
    arg_add = args.add
    arg_chk = args.check
    arg_list = args.list

    if not arg_add and not arg_chk and not arg_list:
      # must choose one command type
      return False

    if arg_add and not arg_chk and not arg_list:
      self.command_type = 'add'
    elif not arg_add and arg_chk and not arg_list:
      self.command_type = 'check'
    elif not arg_add and not arg_chk and arg_list:
      self.command_type = 'list'
      # list doesn't need any extra argument
      return True
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

  def user_exists(self, username):
    ''' check whether the user exists in the password database
        return True if username exists
        return False otherwise
    '''

    return self.password_store.user_exists(username)

  def user_add(self, username, passwd, enc):
    ''' add a user with hashed password '''

    return self.password_store.user_add(username, passwd)

  def user_verify(self, username, passwd, enc_type):
    ''' verify username and hashed password from the password database '''
    
    return self.password_store.user_verify(username, passwd)

  def add_passwd(self):

    user = self.ARGS.user

    if self.user_exists(user):
      print 'User %s already exists.' % user
      return

    passwd_plain = self.ARGS.passwd
    passwd_enc_method = self.ARGS.enc

    passwd_cipher = self.encrypt_passwd(passwd_plain, self.random_string(), passwd_enc_method)

    logger.log('DEBUG', 'password enc method: %s' % passwd_enc_method)
    logger.log('DEBUG', 'password plain text: %s' % passwd_plain)
    logger.log('DEBUG', 'password ciphertext: %s' % passwd_cipher)

    self.user_add(user, passwd_cipher, passwd_enc_method)

    print 'user created'
    print 'add passwd finished'

  def check_passwd(self):

    user = self.ARGS.user

    if not self.user_exists(user):
      print 'User %s does not exist.' % user
      return


    passwd_plain = self.ARGS.passwd
    passwd_enc_method = self.ARGS.enc

    logger.log('DEBUG', 'password enc method: %s' % passwd_enc_method)
    logger.log('DEBUG', 'password plain text: %s' % passwd_plain)

    if self.user_verify(user, passwd_plain, passwd_enc_method):
      print 'Password verified for user %s' % user
    else:
      print 'Password NOT verified for user %s' % user

  def list_passwd(self):
    ''' list all the users' basic information from the database '''
    logger.log('DEBUG', 'Listing all the users from the database...')

    self.password_store.list_users()
    
  @classmethod
  def random_string(cls, length=16):
    char_samples = string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_str = ''.join(random.choice(char_samples) for _ in range(length))
    return random_str

  def encrypt_passwd(self, plaintext, salt, enc_type='ECB'):
    if enc_type != 'ECB' and enc_type != 'CTR' and enc_type != 'CBC':
      return None

    if enc_type == 'ECB':
      cipher = 'ECB' + sha512_crypt.encrypt(plaintext, salt=salt, rounds=5000)
    elif enc_type == 'CTR':
      cipher = 'CTR' + sha512_crypt.encrypt(plaintext, salt=salt, rounds=5000)
    elif enc_type == 'CBC':
      cipher = 'CBC' + sha512_crypt.encrypt(plaintext, salt=salt, rounds=5000)

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
  elif manager.command_type == 'list':
    manager.list_passwd()
  else:
    raise ValueError('Unsupported command type')

if __name__ == '__main__':
  logger = Logger()
  main()

