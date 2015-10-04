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
from struct import pack, unpack, calcsize
from operator import itemgetter


# test data path for phase1
URL_TABLE_IDX = './test_data/phase1_output/url_table.idx'
URL_TABLE_DATA = './test_data/phase1_output/url_table.data'

WORD_TABLE_IDX = './test_data/phase1_output/word_table.idx'
WORD_TABLE_DATA = './test_data/phase1_output/word_table.data'

LEXICON_PATH = './test_data/phase1_output'
SORTED_LEXICON_PATH = './test_data/phase2_output'
# test data path for phase1


class Lexicon(object):
  def __init__(self, lexicon_filename):
    self.lexicon_filename = lexicon_filename
    self.fdr = None

    self.lexicon_list = []

    self.lexicon_schema = 'iiih'
    self.lexicon_lens = calcsize(self.lexicon_schema)

    self.lexicon_output = os.path.join(SORTED_LEXICON_PATH, \
      os.path.basename(lexicon_filename))
    self.fdw = None

  def sort_lexicon(self):
    """ load lexicon, sort it, and write it back """

    self.load()
    self.sort()
    self.save()

  def load(self):
    """ load the lexicon into structured data """

    self.fdr = open(self.lexicon_filename, 'rb')

    rec_len = self.lexicon_lens
    while True:
      lexicon = self.fdr.read(rec_len)
      if lexicon == '':
        return

      word_id, docid, offset, ctx = unpack(self.lexicon_schema, lexicon)
      self.lexicon_list.append({'word_id':word_id, 'docid':docid, 'offset':offset, 'ctx':ctx})

    self.fdr.close()

  def sort(self):
    """ sort the lexicon """
    newlist = sorted(self.lexicon_list, key=itemgetter('word_id'))
    self.lexicon_list = newlist

  def save(self):
    """ write back the structured data back to lexicon """

    self.fdw = open(self.lexicon_output, 'wb')

    for lexicon in self.lexicon_list:
      lexicon_data = pack(self.lexicon_schema, \
        lexicon.get('word_id'), lexicon.get('docid'), \
        lexicon.get('offset'), lexicon.get('ctx'))
      self.fdw.write(lexicon_data)
    
    self.fdw.close()


def get_lexicon_files():
  """ get a list of lexicon full path filenames """
  glob_path = os.path.join(LEXICON_PATH, '*.lexicon')
  return glob.glob(glob_path)

def sort_lexicon(filename):
  """ sort lexicon based on word_id, docid
      INPUT: unsorted lexicon file (*.lexicon)
      OUTPUT: sorted lexicon file (*.lexicon.sorted)
  """
  lex = Lexicon(filename)
  lex.sort_lexicon()

def main():
  """ main routine """
  for lexicon in get_lexicon_files():
    sort_lexicon(lexicon)


if __name__ == '__main__':
  main()

