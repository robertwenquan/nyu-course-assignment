#!/usr/bin/python

"""
sort generated lexicon

For each lexicon files generated from raw input
sort it based on word_id, doc_id, offset, context

 LEXICON(14B)
 - word id(4B)
 - doc id(4B)
 - offset to content(4B)
 - context(2B)

"""

import os
import glob


# test data path for phase1
URL_TABLE_IDX = './test_data/phase1_output/url_table.idx'
URL_TABLE_DATA = './test_data/phase1_output/url_table.data'

WORD_TABLE_IDX = './test_data/phase1_output/word_table.idx'
WORD_TABLE_DATA = './test_data/phase1_output/word_table.data'

LEXICON_PATH = './test_data/phase1_output'
SORTED_LEXICON_PATH = './test_data/phase2_output'
# test data path for phase1


def get_lexicon_files():
  """ get a list of lexicon full path filenames """
  glob_path = os.path.join(LEXICON_PATH, '*.lexicon')
  return glob.glob(glob_path)


def main():
  """ main routine """
  for lexicon in get_lexicon_files():
    print lexicon


if __name__ == '__main__':
  main()

