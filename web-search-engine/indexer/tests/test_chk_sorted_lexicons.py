#!/usr/bin/env python

"""
check sorted lexicon files

 LEXICON(14B)
 - word id(4B)
 - doc id(4B)
 - offset to content(4B)
 - context(2B)
"""

import os
import glob
from struct import calcsize, unpack
from unittest import TestCase

SORTED_LEXICONS_PATH = 'test_data/phase2_output'

class TestVerifySortedLexicons(TestCase):

  def test_check_sorted_lexicons(self):
    """ check sorted lexicon files """

    lexicon_schema = 'iiih'
    rec_size = calcsize(lexicon_schema)

    print 'Lexicons...'
    print '[word_id][docid][offset][context]'

    files = glob.glob(os.path.join(SORTED_LEXICONS_PATH, '*.lexicon'))
    for lex_file in files:
      with open(lex_file, 'rb') as fdr:
        cnt = 0
        while cnt < 10:
          data = fdr.read(rec_size)
          if data == '':
            break
          print lex_file, unpack(lexicon_schema, data)
          cnt += 1


if __name__ == '__main__':
  TestVerifySortedLexicons.run()

