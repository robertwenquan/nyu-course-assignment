#!/usr/bin/env python

"""
generate inverted index based on the output of phase2
for each sorted lexicon file, a set of three index files will be created.
Let's call them (global index table, middle index table, and inverted index)
                 GIT, MIT, IIDX

# INPUT SCHEMA DEFINED AS BELOW:

LEXICON(14B)
 - word id(4B)
 - doc id(4B)
 - offset to content(4B)
 - context(2B)

# OUTPUT SCHEMA DEFINED AS BELOW:

Global INDEX (10B)
 - word id(4B)
 - offset(4B)     # offset in the middle INDEX
 - occurrence(2B) # meaning the word has occurrences in N documents

Middle INDEX (10B)
 - docid(4B)      # this entry is for doc associated with this docid
 - offset(4B)     # offset in the inverted index file
 - occurrence(2B) # meaning the word has N occurrences in the doc[docid]

Inverted INDEX (4B per entry)
 - offset1(4B)
 - offset2(4B)
 - ...    (4B)
 - offsetN(4B)

"""

import os
import glob
from struct import pack, unpack, calcsize


BASE_DIR = '/data/wse/100k'
BASE_DIR = './test_data'

# test data path for phase2
SORTED_LEXICON_PATH = os.path.join(BASE_DIR, 'phase2_output')
INVERTED_INDEX_PATH = os.path.join(BASE_DIR, 'phase3_output')
# test data path for phase2


class InvertedIndex(object):
  """ class for inverted index table """

  def __init__(self, lexicon_filename):
    self.lexicon_filename = lexicon_filename
    self.fdr = None

    self.lex_schema = 'iiih'
    self.git_schema = 'iih'
    self.mit_schema = 'iih'
    self.iidx_schema = 'i'

    self.output_git = os.path.join(INVERTED_INDEX_PATH, \
      '.'.join(os.path.basename(lexicon_filename).split('.')[:-1]+['git']))
    self.output_mit = os.path.join(INVERTED_INDEX_PATH, \
      '.'.join(os.path.basename(lexicon_filename).split('.')[:-1]+['mit']))
    self.output_iidx = os.path.join(INVERTED_INDEX_PATH, \
      '.'.join(os.path.basename(lexicon_filename).split('.')[:-1]+['iidx']))

    self.fdw_git = open(self.output_git, 'wb')
    self.fdw_mit = open(self.output_mit, 'wb')
    self.fdw_iidx = open(self.output_iidx, 'wb')

  def iter_lexicon(self):
    """ iterator for lexicons """
    offset = 0
    rec_size = calcsize(self.lex_schema)

    self.fdr = open(self.lexicon_filename)
    while True:
      data = self.fdr.read(rec_size)
      if data == '':
        break
      yield unpack(self.lex_schema, data)

    self.fdr.close()

  def write_iidx(self, data):
    self.fdw_iidx.write(data)

  def write_mit(self, data):
    self.fdw_mit.write(data)

  def write_git(self, data):
    self.fdw_git.write(data)

  def run(self):
    word_id_curr = docid_curr = -1
    count_in_mit = count_in_git = 0
    offset_in_mit = offset_in_git = 0

    for lexicon in self.iter_lexicon():
      word_id, docid, offset, ctx = lexicon
      #print word_id, docid, offset, ctx

      # word_id and docid initialization
      if word_id_curr == -1:
        word_id_curr = word_id
      if docid_curr == -1:
        docid_curr = docid

      # when data from new word comes
      # write back mit first
      # then write back git
      if word_id != word_id_curr:

        # write back mit
        print 'write MIT entry:', self.mit_schema, word_id_curr, docid_curr, offset_in_mit, count_in_mit
        data_mit = pack(self.mit_schema, docid_curr, offset_in_mit, count_in_mit)
        self.write_mit(data_mit)
        count_in_git += 1

        docid_curr = docid
        offset_in_mit = self.fdw_iidx.tell()
        count_in_mit = 1

        # write back git
        print 'write GIT entry:', self.git_schema, word_id_curr, docid_curr, offset_in_git, count_in_git
        data_git = pack(self.git_schema, word_id_curr, offset_in_git, count_in_git)
        self.write_git(data_git)

        word_id_curr = word_id
        offset_in_git = self.fdw_mit.tell()
        count_in_git = 0

        # write the inverted index
        print 'write INDEX entry:', self.iidx_schema, word_id_curr, docid_curr, offset
        data_iidx = pack(self.iidx_schema, offset)
        self.write_iidx(data_iidx)

        continue

      # when data from new doc comes, write back in mit
      # for the previous doc, with
      # (docid, offset, n_occur)
      # where offset is the start offset for this doc
      # and n_occur is number of occurrences of the word in this doc
      if docid != docid_curr:
        print 'write MIT entry:', self.mit_schema, word_id_curr, docid_curr, offset_in_mit, count_in_mit
        data_mit = pack(self.mit_schema, docid_curr, offset_in_mit, count_in_mit)
        self.write_mit(data_mit)
        count_in_git += 1

        docid_curr = docid
        offset_in_mit = self.fdw_iidx.tell()
        count_in_mit = 1

        # write the inverted index
        print 'write INDEX entry:', self.iidx_schema, word_id_curr, docid_curr, offset
        data_iidx = pack(self.iidx_schema, offset)
        self.write_iidx(data_iidx)

        continue
      
      # write the inverted index
      print 'write INDEX entry:', self.iidx_schema, word_id_curr, docid_curr, offset
      data_iidx = pack(self.iidx_schema, offset)
      self.write_iidx(data_iidx)

      count_in_mit += 1

    else:

      print 'write MIT entry:', self.mit_schema, word_id_curr, docid_curr, offset_in_mit, count_in_mit
      data_mit = pack(self.mit_schema, docid_curr, offset_in_mit, count_in_mit)
      self.write_mit(data_mit)

      # write back git
      count_in_git += 1
      print 'write GIT entry:', self.git_schema, word_id_curr, docid_curr, offset_in_git, count_in_git
      data_git = pack(self.git_schema, word_id_curr, offset_in_git, count_in_git)
      self.write_git(data_git)

def get_lexicon_files():
  """ get a list of lexicon full path filenames """
  glob_path = os.path.join(SORTED_LEXICON_PATH, '*.lexicon')
  return glob.glob(glob_path)

def process_lexicon(filename):
  """ process sorted lexicon file to inverted index files
      INPUT: sorted lexicon file (*.lexicon)
      OUTPUT: inverted index files
              - *.git
              - *.mit
              - *.iidx
  """
  lex = InvertedIndex(filename)
  lex.run()


def main():
  """ main routine """

  for lexicon in get_lexicon_files():
    process_lexicon(lexicon)


if __name__ == '__main__':
  main()

