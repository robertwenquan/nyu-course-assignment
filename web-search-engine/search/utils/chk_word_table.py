#!/usr/bin/env python

"""
list all the wordid - word mapping

Sample usage:
$ python utils/chk_word_table.py


word id index entry format
{
[4 B] word id
[4 B] offset of the word
[1 B] length of the word
}

word table entry format
{
[N B] N as read from the above
}

"""

from struct import calcsize
from struct import unpack
import os
import sys


BASE_DIR = './test_data'

WORD_TABLE_IDX = '/tmp/word_table.idx'
WORD_TABLE_DATA = '/tmp/word_table.data'

WORD_TABLE_IDX = os.path.join(BASE_DIR, 'output/word_table.idx')
WORD_TABLE_DATA = os.path.join(BASE_DIR, 'output/word_table.data')


def main():
  """ main routine """

  word_idx_schema = 'iiB'
  
  # record length
  idx_len = calcsize(word_idx_schema)
  rec_len = calcsize('B')

  try:
    fd_word_idx = open(WORD_TABLE_IDX)
    fd_word_data = open(WORD_TABLE_DATA)

    # iterate word index table
    # and fetch word string frmo the word data table
    while True:
      idx_data = fd_word_idx.read(idx_len)
      if idx_data == '':
        break

      word_id, offset, word_lens = unpack(word_idx_schema, idx_data)

      fd_word_data.seek(offset)
      word_str = fd_word_data.read(word_lens)
      print word_id, word_str

  except IOError:
    # to handle the piped output to head
    # like check_word_table.py | head
    fd_word_idx.close()
    fd_word_data.close()


if __name__ == '__main__':

  main()

