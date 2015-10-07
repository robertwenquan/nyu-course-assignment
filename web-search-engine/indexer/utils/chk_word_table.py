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
[1 B] length of the word
[N B] N as read from the above
}

Iterate until the end of the file
"""

from struct import calcsize
import os
import sys


BASE_DIR = './test_data'

WORD_TABLE_IDX = '/tmp/word_table.idx'
WORD_TABLE_DATA = '/tmp/word_table.data'

WORD_TABLE_IDX = os.path.join(BASE_DIR, 'phase1_output/word_table.idx')
WORD_TABLE_DATA = os.path.join(BASE_DIR, 'phase1_output/word_table.data')


def main():
  """ main routine """

  # not reading index table
  #word_idx_schema = 'iiB'
  
  # record length in the word data table
  rec_len = calcsize('B')

  try:
    with open(WORD_TABLE_DATA) as fd_word_data:
      while True:
        data = fd_word_data.read(rec_len)
        if data == '':
          break
  
        word_len = ord(data)
        word_str = fd_word_data.read(word_len)
        print word_str
  except IOError:
    # to handle the piped output to head
    # like check_word_table.py | head
    fd_word_data.close()


if __name__ == '__main__':

  if os.path.exists(sys.argv[1]):
    WORD_TABLE_DATA = sys.argv[1]

  main()

