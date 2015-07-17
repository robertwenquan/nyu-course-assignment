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
 1. Install Python 2.7 (only run and tested with Python 2.7)
 2. Install pip
 3. Install dependencies
    $ pip install -r requirements.txt

Example:
 ./pwmgr.py --help
 ./pwmgr.py -a -u <username> -p <password> -e [ECB,CTR,CBC]
 ./pwmgr.py -c -u <username> -p <password> -e [ECB,CTR,CBC]
 ./pwmgr.py -l
 ./pwmgr.py -d -u <username>
"""

import os
import sys
import random
import string
import sqlite3
import argparse
from Crypto.Hash import SHA
from Crypto.Cipher import AES
from Crypto.Util import Counter


MASTER_KEY_FILE = '~/.pwmgr.key'
INITIALIZATION_VECTOR = 'r3GK7xVX4v16VKjJ'
PADDING_BYTE = '0'

class Logger(object):
  '''
  unified logger
  '''

  enable_debug = False

  def log(self, loglevel, log_string):
    ''' log function '''
    if loglevel.upper() == 'DEBUG' and self.enable_debug == True:
      print log_string


class PasswordStore(object):
  '''
  password store, backed by sqlite
  '''

  def __init__(self):
    self.connection = sqlite3.connect('passwd_manager.db')
    self.connection.isolation_level = None
    self.create_table_if_not_exist()

  def create_table_if_not_exist(self):
    ''' create table 'shadow' if it does not exist '''
    cur = self.connection.cursor()
    sql_statmt = 'CREATE TABLE IF NOT EXISTS shadow (username varchar(32), passwd varchar(64))'
    cur.execute(sql_statmt)

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

  def user_purge(self):
    ''' remove all password entries from the database '''
    ''' TESTING ONLY '''
    cur = self.connection.cursor()
    sql_statmt = "DELETE from shadow"
    cur.execute(sql_statmt)

  def user_info_fetch(self, username):
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
    _, _, salt_key, _ = cipher_fetched.split('$')

    salt_key = str(salt_key)
    full_hashed_key = str(cipher_fetched)

    return salt_key, full_hashed_key

  def list_users(self):
    ''' list all users from the databases '''

    cur = self.connection.cursor()
    sql_statmt = "SELECT username, passwd FROM shadow"
    cur.execute(sql_statmt)

    for (user, passwd) in cur.fetchall():
      enc = passwd.split('$')[1]
      salt = passwd.split('$')[2]
      encrypted = passwd.split('$')[3]
      print "%10s %3s %16s %s" % (user, enc, salt, encrypted)

  def del_user(self, username):
    ''' delete user password entry from database '''

    cur = self.connection.cursor()
    sql_statmt = "DELETE from shadow WHERE username = '%s'" % username
    cur.execute(sql_statmt)


class PasswordManager(object):
  '''
  class for global password manager
  '''

  args = None
  command_type = ''
  masterkey = ''
  logger = Logger()

  def __init__(self, argv):
    self.args = self.init_args(argv)
    self.password_store = PasswordStore()
    self.masterkey = self.init_masterkey()

  def init_args(self, argv):
    ''' initialize arguments '''

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', action='store_true', help='add password into database')
    parser.add_argument('-c', '--check', action='store_true', help='check password validity')
    parser.add_argument('-l', '--list', action='store_true', \
        help='list users from the password database')
    parser.add_argument('-d', '--dele', action='store_true', \
        help='remove user from the password database')
    parser.add_argument('-u', '--user', default=None, help='username')
    parser.add_argument('-p', '--passwd', default=None, help='password')
    parser.add_argument('-e', '--enc', default='ECB', \
        help='cipher text encryption method. ECB|CTR|CBC')
    parser.add_argument('-x', '--debug', action='store_true', help='enable debugging output')

    args = parser.parse_args(argv)

    # set logger DEBUG flag
    if args.debug:
      self.logger.enable_debug = True

    # print arguments
    self.logger.log('DEBUG', 'argument check: --add %s' % args.add)
    self.logger.log('DEBUG', 'argument check: --check %s' % args.check)
    self.logger.log('DEBUG', 'argument check: --list %s' % args.list)
    self.logger.log('DEBUG', 'argument check: --dele %s' % args.dele)
    self.logger.log('DEBUG', 'argument check: --user %s' % args.user)
    self.logger.log('DEBUG', 'argument check: --passwd %s' % args.passwd)

    check_status = self.check_args(args)
    if not check_status:
      parser.print_help()
      exit(2)

    return args

  def init_masterkey(self):
    ''' init masterkey '''

    writeback = False

    try:
      filename = os.path.expanduser(MASTER_KEY_FILE)
      masterkey = open(filename).read()
    except:
      masterkey = self.random_string(32)
      writeback = True

    if writeback:
      try:
        open(filename, 'w').write(masterkey)
      except:
        return None

    return masterkey

  def check_args(self, args):
    ''' validate command line arguments '''

    # check command type
    arg_add = args.add
    arg_chk = args.check
    arg_list = args.list
    arg_del = args.dele

    if not arg_add and not arg_chk and not arg_list and not arg_del:
      # must choose one command type
      return False

    if arg_add and not arg_chk and not arg_list and not arg_del:
      self.command_type = 'add'
    elif not arg_add and arg_chk and not arg_list and not arg_del:
      self.command_type = 'check'
    elif not arg_add and not arg_chk and arg_list and not arg_del:
      self.command_type = 'list'
      # list doesn't need any extra argument
      return True
    elif not arg_add and not arg_chk and not arg_list and arg_del:
      self.command_type = 'del'
    else:
      # only one command type could be selected
      return False

    # check user and pass
    arg_user = args.user
    arg_pass = args.passwd

    if arg_del and arg_user:
      # --dele only needs --user
      return True

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

  def user_add(self, username, passwd):
    ''' add a user with hashed password '''

    return self.password_store.user_add(username, passwd)

  def user_verify(self, username, password, enc_method):
    ''' verify username and hashed password from the password database '''

    self.logger.log('DEBUG', 'username: %s' % username)
    self.logger.log('DEBUG', 'password: %s' % password)

    salt, saved_encrypted_password = self.password_store.user_info_fetch(username)
    self.logger.log('DEBUG', 'salt: %s (%d) (%s)' % (salt, len(salt), type(salt)))
    self.logger.log('DEBUG', 'hashed0: %s (%d) (%s)' % (saved_encrypted_password, \
        len(saved_encrypted_password), \
        type(saved_encrypted_password)))

    # recalculate the crypted one
    cipher_recalculated = self.encrypt_passwd(password, salt, enc_method)
    self.logger.log('DEBUG', 'hashed1: %s' % cipher_recalculated)

    # compare them
    if cipher_recalculated == saved_encrypted_password:
      return True
    else:
      return False

  def add_passwd(self):
    ''' add a password to the database '''

    user = self.args.user

    if self.user_exists(user):
      print 'User %s already exists.' % user
      return

    passwd_plain = self.args.passwd
    passwd_enc_method = self.args.enc

    passwd_cipher = self.encrypt_passwd(passwd_plain, self.random_string(), passwd_enc_method)

    self.logger.log('DEBUG', 'password enc method: %s' % passwd_enc_method)
    self.logger.log('DEBUG', 'password plain text: %s' % passwd_plain)
    self.logger.log('DEBUG', 'password ciphertext: %s' % passwd_cipher)

    self.user_add(user, passwd_cipher)

    print 'user %s with password is created.' % user

  def check_passwd(self):
    ''' check the validity of the password '''

    user = self.args.user

    if not self.user_exists(user):
      print 'User %s does not exist.' % user
      return None

    passwd_plain = self.args.passwd
    passwd_enc_method = self.args.enc

    self.logger.log('DEBUG', 'password enc method: %s' % passwd_enc_method)
    self.logger.log('DEBUG', 'password plain text: %s' % passwd_plain)

    if self.user_verify(user, passwd_plain, passwd_enc_method):
      print 'Password verified for user %s' % user
      return True
    else:
      print 'Password NOT verified for user %s' % user
      return False

  def list_passwd(self):
    ''' list all the users' basic information from the database '''
    self.logger.log('DEBUG', 'Listing all the users from the database...')

    self.password_store.list_users()

  def del_passwd(self):
    ''' delete the user from the password database '''

    user = self.args.user

    if not self.user_exists(user):
      print 'User %s does not exist.' % user
      return

    self.logger.log('DEBUG', 'removing %s from password database.' % user)
    print 'user %s deleted from database' % user
    self.password_store.del_user(user)

  def del_all(self):
    ''' delete all user entries from the database '''
    ''' ONLY for unit testing '''
    self.password_store.user_purge()

  @classmethod
  def random_string(cls, length=16):
    ''' generate random text string with specified byte length'''
    char_samples = string.ascii_uppercase + string.ascii_lowercase + string.digits
    random_str = ''.join(random.choice(char_samples) for _ in range(length))
    return random_str

  def encrypt_passwd(self, plaintext, salt, enc_type='ECB'):
    ''' encrypt the plaintext password with specified algorithm (ECB, CTR, CBC)
        the plaintext password will be first encrypted with the masterkey with
        the specified encryption alrorithm
        then a salt will be appended to the encrypted key
        and a final hashed key string will be computed against the combined string

        the full stored password entry is composed of three elements:
        encryption method, salt, hashed string
        they are separated by '$', with an additional leading '$' at the beginning
    '''

    if enc_type != 'ECB' and enc_type != 'CTR' and enc_type != 'CBC':
      return None

    if enc_type == 'ECB':
      enc_method = AES.MODE_ECB
    elif enc_type == 'CTR':
      enc_method = AES.MODE_CTR
    elif enc_type == 'CBC':
      enc_method = AES.MODE_CBC

    ctr = Counter.new(128)
    iv = INITIALIZATION_VECTOR
    key = self.masterkey

    if enc_method == AES.MODE_CTR:
      # counter is only for MODE_CTR, couldn't be called with CBC or ECB
      encoder = AES.new(key, enc_method, counter=ctr)
    elif enc_method == AES.MODE_CBC:
      # iv is only for CBC, though it will be ignored by CTR and ECB
      encoder = AES.new(key, enc_method, iv)
    elif enc_method == AES.MODE_ECB:
      encoder = AES.new(key, enc_method)

    self.logger.log('DEBUG', 'plaintext: %s' % plaintext)
    cipher = encoder.encrypt(plaintext + ((16 - len(plaintext)%16) * PADDING_BYTE))
    self.logger.log('DEBUG', 'cipher: %s' % cipher)

    hashed_cipher = SHA.new(cipher + str(salt)).hexdigest()
    self.logger.log('DEBUG', 'hashed_cipher: %s' % hashed_cipher)
    password_full_entry = '$%s$%s$%s' % (enc_type, salt, hashed_cipher)
    self.logger.log('DEBUG', 'password_entry: %s' % password_full_entry)

    return password_full_entry


def main():

  manager = PasswordManager(sys.argv[1:])

  if manager.command_type == 'add':
    manager.add_passwd()
  elif manager.command_type == 'check':
    manager.check_passwd()
  elif manager.command_type == 'list':
    manager.list_passwd()
  elif manager.command_type == 'del':
    manager.del_passwd()
  else:
    raise ValueError('Unsupported command type')

if __name__ == '__main__':
  main()

