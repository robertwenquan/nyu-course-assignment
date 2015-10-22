#!/usr/bin/env python

"""
list all the wordid - word mapping

Sample usage:
$ python utils/chk_word_table.py


 URL_TABLE_ENTRY(28B)
 - docid(4B)
 - loc of url(8B)
  - url fileid(2B)
  - url offset(4B)
  - url length(2B)
 - loc of doc(16B)
  - wet fileid(2B)
  - offset in the file(4B)
  - length of the file including header(4B)
  - content start offset from the doc(2B)
  - content length(4B)

 URL_ENTRY(VARIABLE LENGTH)
 - url(variable length)

"""

from struct import calcsize
from struct import unpack
import os
import sys


BASE_DIR = './test_data'

URL_TABLE_IDX = os.path.join(BASE_DIR, 'output/url_table.idx')
URL_TABLE_DATA = os.path.join(BASE_DIR, 'output/url_table.data')


def main():
  """ main routine """

  url_idx_schema = 'ihihhiihi'
  
  # record length
  idx_len = calcsize(url_idx_schema)

  try:
    fd_url_idx = open(URL_TABLE_IDX)
    fd_url_data = open(URL_TABLE_DATA)

    # iterate word index table
    # and fetch word string frmo the word data table
    while True:
      idx_data = fd_url_idx.read(idx_len)
      if idx_data == '':
        break

      docid, _, offset, length, _, _, _, _, _ = unpack(url_idx_schema, idx_data)

      fd_url_data.seek(offset)
      url_str = fd_url_data.read(length)
      print docid, url_str

  except IOError:
    # to handle the piped output to head
    # like check_word_table.py | head
    fd_url_idx.close()
    fd_url_data.close()


if __name__ == '__main__':

  main()

