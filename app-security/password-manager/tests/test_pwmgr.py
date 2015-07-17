#!/usr/bin/env python

import unittest
from pwmgr import PasswordStore

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

  def test_add_user(self):
    print 'add user test'

  def test_check_user(self):
    print 'check user test'

if __name__ == '__mani__':
  unittest.main()

