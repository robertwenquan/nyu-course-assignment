#!/usr/bin/env python

"""
Scan over the WET files and generate the first pass information
- URL table
- WORD table
- LEXICON per WET file


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
 - length of url(2B)
 - url(variable length)

 LEXICON(14B)
 - word id(4B)
 - doc id(4B)
 - offset to content(4B)
 - context(2B)

 WORD_TABLE_ENTRY(9B)
 - word_id(4B)
 - loc of word(5B)
  - word offset(4B)
  - word length(1B)

 WORD_ENTRY(VARIABLE LENGTH)
 - word(variable length)

"""

import os
import re
import glob
import warc
from struct import pack


# test dataset with 30k docs
BASE_DIR = './test_data'

# bigger dataset with 100k docs
#BASE_DIR = '/data/wse/100k'

WET_DIR = os.path.join(BASE_DIR, 'input')
URL_TABLE_IDX = os.path.join(BASE_DIR, 'phase1_output/url_table.idx')
URL_TABLE_DATA = os.path.join(BASE_DIR, 'phase1_output/url_table.data')

WORD_TABLE_IDX = os.path.join(BASE_DIR, 'phase1_output/word_table.idx')
WORD_TABLE_DATA = os.path.join(BASE_DIR, 'phase1_output/word_table.data')

LEXICON_PATH = os.path.join(BASE_DIR, 'phase1_output')
# bigger dataset

def get_wet_files():
  """ get a list of wet full path filenames """
  glob_path = os.path.join(WET_DIR, '*.wet')
  file_list = glob.glob(glob_path)
  return sorted(file_list)

def docid_generator():
  """ generate docid from 1 and upwards """
  docid = 0
  while True:
    docid += 1
    yield docid

def wordid_generator():
  """ generate wordid from 1 and upwards """
  wordid = 0
  while True:
    wordid += 1
    yield wordid

def is_ascii(s):
  return all(ord(c) < 128 for c in s)

def split_with_offset(line, _len=len):
  """ split string to tokens with offset """
  words = re.split('[ ,.:!"|(){}\t\n]', line)
  index = line.index
  offsets = []
  append = offsets.append
  running_offset = 0
  for word in words:
    word_offset = index(word, running_offset)
    word_len = _len(word)
    running_offset = word_offset + word_len
    append((word, word_offset, running_offset - 1))
  return offsets


class UrlIndex(object):
  """ class for handling URL table index """

  def __init__(self):
    self.url_index_file = URL_TABLE_IDX
    self.url_index_data = URL_TABLE_DATA
    self.url_index_offset = 0

    self.fd_url_idx = open(self.url_index_file, 'wb')
    self.fd_url_data = open(self.url_index_data, 'wb')

  def write_url_index(self, url):
    """ write URLs index into file """
    url_lens = len(url)
    fileid = 99
    offset = self.url_index_offset
    self.url_index_offset += (2 + url_lens)

    # write-back format: len(2B), url as string
    url_lens_data = pack('h', url_lens)
    self.fd_url_data.write(url_lens_data)
    self.fd_url_data.write(url)

    return (url_lens, fileid, offset)

  def write_url_index_entry(self, data):
    self.fd_url_idx.write(data)


class WordIndex(UrlIndex):
  """ class for word id and index """

  def __init__(self):
    self.word_table = {}

    self.word_index_file = WORD_TABLE_IDX
    self.word_index_data = WORD_TABLE_DATA
    self.word_index_offset = 0

    self.fd_word_data = open(self.word_index_data, 'wb')
    self.fd_word_idx = open(self.word_index_file, 'wb')

    self.wordid_gen = wordid_generator()

  def get_word_id(self, word):
    """ get word_id based on word
        return existing word_id if exists
        otherwise generate new word_id
    """
    word_id = self.word_table.get(word)
    if word_id:
      return word_id, False
    else:
      word_id = self.wordid_gen.next()
      self.word_table[word] = word_id
      return word_id, True

  def add_entry(self, word):
    word_lens = len(word)
    offset = self.word_index_offset
    self.word_index_offset += word_lens

    # get word_id
    word_id, new_id = self.get_word_id(word)
    if not new_id:
      return word_id

    # write-back format: word as string
    self.fd_word_data.write(word)

    # write back index entry
    word_id_index_data = pack('iiB', word_id, offset, word_lens)
    self.fd_word_idx.write(word_id_index_data)

    return word_id


def main():
  """ main routine """

  wet_files = get_wet_files()
  docid_gen = docid_generator()

  url_index = UrlIndex()
  word_index = WordIndex()

  for wet_file in wet_files:
    print wet_file
    wet_fd = warc.open(wet_file)
    doc_next_offset = 0

    lexicon_file = os.path.join(LEXICON_PATH, '.'.join(os.path.basename(wet_file).split('.')[:-1] + ['lexicon']))
    lex_fd = open(lexicon_file, 'wb')

    for wet_record in wet_fd:
      if wet_record.url:

        docid = docid_gen.next()

        url = wet_record.url
        url_lens, url_fileid, url_offset = url_index.write_url_index(url)

        doc_fileid = 88
        doc_offset = doc_next_offset if doc_next_offset else 0
        doc_header_length = wet_record.payload.fileobj.tell() - doc_offset
        doc_length = doc_header_length + wet_record.header.content_length

        content_offset = doc_header_length
        content_length = wet_record.header.content_length

        print docid, url, (url_fileid, url_offset, url_lens), \
          (doc_fileid, doc_offset, doc_length, content_offset, content_length)

        # docid(4B), url_pos[fileid(2B), offset(4B), lens(2B)],
        # doc_pos[fileid(2B), offset(4B), lens(4B), con_offset(2B), con_lens(4B)]
        url_idx_data = pack('ihihhiihi', \
                        docid, url_fileid, url_offset, url_lens, doc_fileid, \
                        doc_offset, doc_length, content_offset, content_length)
        url_index.write_url_index_entry(url_idx_data)

        # generate lexicons
        saved_offset = wet_record.payload.fileobj.tell()
        page_content = wet_record.payload.fileobj.read(content_length)
        wet_record.payload.fileobj.seek(saved_offset)
        for token, start, end in split_with_offset(page_content):
          if is_ascii(token) and len(token) > 0 and len(token) < 256:
            word_id = word_index.add_entry(token)
            lexicon_data = pack('iiih', word_id, docid, start, 2)
            lex_fd.write(lexicon_data)

        doc_next_offset = wet_record.payload.fileobj.tell() + wet_record.payload.length

    lex_fd.close()
    wet_fd.close()


if __name__ == '__main__':
  main()

