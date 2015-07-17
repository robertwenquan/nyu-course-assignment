#!/usr/bin/env python

"""
unittests for the password manager

tested the password store, which is the sqlite3 storage
and the password manager, for adding and checking user password
"""

import unittest
from pwmgr import PasswordStore
from pwmgr import PasswordManager
from pwmgr import Logger

class TestPasswordMgr(unittest.TestCase):

  def test_password_store(self):

    pw_store = PasswordStore()

    # remove all password entries
    pw_store.user_purge()

    # test for non-existing users
    for userid in range(1,11):
      username = 'user_not_exist_' + str(userid)
      self.assertTrue(pw_store.user_exists(username) == False)

    # add a few users and test the validity
    for userid in range(1,6):
      username = 'user_valid_' + str(userid)
      password = '$CBC$salt_salt_salt$passwd_valid_' + str(userid)
      pw_store.user_add(username, password)
      self.assertTrue(pw_store.user_exists(username) == True)
      salt, pwstr = pw_store.user_info_fetch(username)
      self.assertTrue(salt == 'salt_salt_salt')
      self.assertTrue(pwstr == password)

    # list users
    pw_store.list_users()

    # del users
    for userid in range(1,6):
      username = 'user_valid_' + str(userid)
      self.assertTrue(pw_store.user_exists(username) == True)
      pw_store.del_user(username)
      self.assertTrue(pw_store.user_exists(username) == False)

    # list users
    pw_store.list_users()

    pw_store = None

  def test_add_and_verify_user(self):
    ''' test add user function by password manager '''

    # purge the database
    manager = PasswordManager(['-l'])
    manager.del_all()

    # create a user 'sample_user' with password 'sample_password'
    # with default ECB encryption
    username = 'sample_user'
    password = 'sample_password'

    args = ['-a', '-u', username, '-p', password]
    manager = PasswordManager(args)
    manager.add_passwd()
    self.assertTrue(manager.password_store.user_exists(username) == True)

    args = ['-c', '-u', username, '-p', password]
    manager = PasswordManager(args)
    self.assertTrue(manager.check_passwd() == True)

    # create 3 x 99 users with three password encryption methods
    for userid in range(1,100):
      for enc_method in ['CTR', 'ECB', 'CBC']:
        username = 'user_valid_' + str(userid) + str(enc_method)
        args = ['-a', '-u', username, '-p', 'password', '-e', enc_method]
        manager = PasswordManager(args)
        manager.add_passwd()
        self.assertTrue(manager.password_store.user_exists(username) == True)

    # verify password with the 3 x 99 users
    for userid in range(1,100):
      for enc_method in ['CTR', 'ECB', 'CBC']:
        username = 'user_valid_' + str(userid) + str(enc_method)
        args = ['-c', '-u', username, '-p', 'password', '-e', enc_method]
        manager = PasswordManager(args)
        self.assertTrue(manager.check_passwd() == True)


if __name__ == '__main__':
  unittest.main()

