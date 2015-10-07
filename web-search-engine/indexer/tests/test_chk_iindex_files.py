#!/usr/bin/env python

"""
check inverted index files before merge
"""

import os
import glob
from struct import calcsize, unpack
from unittest import TestCase

INVERTED_INDEX_PATH = 'test_data/phase3_output'

class TestVerifyInvertedIndex(TestCase):

  def test_check1_global_index_table(self):
    """ check global index table """

    git_schema = 'iih'
    rec_size = calcsize(git_schema)

    print 'Global Index Table...'
    print '[word_id][offset][occurrences]'

    files = glob.glob(os.path.join(INVERTED_INDEX_PATH, '*.git'))
    for git_file in files:
      with open(git_file, 'rb') as fdr:
        cnt = 0
        while cnt < 5:
          data = fdr.read(rec_size)
          if data == '':
            break
          print git_file, unpack(git_schema, data)
          cnt += 1

  def test_check2_middle_index_table(self):
    """ check middle index table """

    mit_schema = 'iih'
    rec_size = calcsize(mit_schema)

    print 'Middle Index Table...'
    print '[docid][offset][occurrences]'

    files = glob.glob(os.path.join(INVERTED_INDEX_PATH, '*.mit'))
    for mit_file in files:
      with open(mit_file, 'rb') as fdr:
        cnt = 0
        while cnt < 10000:
          data = fdr.read(rec_size)
          if data == '':
            break
      
          docid, offset, occur = unpack(mit_schema, data)
          self.assertTrue(occur > 0)
          print mit_file, docid, offset, occur
          cnt += 1

  def test_check3_iindex_table(self):
    """ check inverted index table """

    iidx_schema = 'i'
    rec_size = calcsize(iidx_schema)

    print 'Inverted Index...'
    print '[offset]'

    files = glob.glob(os.path.join(INVERTED_INDEX_PATH, '*.iidx'))
    for iidx_file in files:
      with open(iidx_file, 'rb') as fdr:
        cnt = 0
        while cnt < 10:
          data = fdr.read(rec_size)
          if data == '':
            break
          print iidx_file, unpack(iidx_schema, data)[0]
          cnt += 1


if __name__ == '__main__':
  TestVerifyInvertedIndex.run()

