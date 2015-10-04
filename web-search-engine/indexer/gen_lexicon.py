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

 WORD_TABLE_ENTRY(10B)
 - word_id(4B)
 - loc of word(6B)
  - word offset(4B)
  - word length(2B)

 WORD_ENTRY(VARIABLE LENGTH)
 - length of word
 - word(variable length)

"""

import os
import glob
import warc
from struct import pack


WET_DIR = '/tmp/cc201507/'
URL_TABLE_IDX = '/tmp/url_table.idx'
URL_TABLE_URLS = '/tmp/url_table.urls'

LEXICON_PATH = '/tmp'


def get_wet_files():
  """ get a list of wet full path filenames """
  glob_path = os.path.join(WET_DIR, '*.wet')
  return glob.glob(glob_path)

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
  words = line.split()
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
    self.url_index_urls = URL_TABLE_URLS
    self.url_index_offset = 0

    self.fd_urls = open(self.url_index_urls, 'wb')
    self.fd_url_idx = open(self.url_index_file, 'wb')

  def write_url_index(self, url):
    """ write URLs index into file """
    url_lens = len(url)
    fileid = 99
    offset = self.url_index_offset
    self.url_index_offset += (2 + url_lens)

    # write-back format: len(2B), url as string
    url_lens_data = pack('h', url_lens)
    self.fd_urls.write(url_lens_data)
    self.fd_urls.write(url)

    return (url_lens, fileid, offset)

  def write_url_index_entry(self, data):
    self.fd_url_idx.write(data)


def main():
  """ main routine """

  wet_files = get_wet_files()
  docid_gen = docid_generator()
  wordid_gen = wordid_generator()

  url_index = UrlIndex()

  for wet_file in wet_files:
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
          if is_ascii(token):
            word_id = wordid_gen.next()
            lexicon_data = pack('iiih', word_id, docid, start, 2)
            lex_fd.write(lexicon_data)

        doc_next_offset = wet_record.payload.fileobj.tell() + wet_record.payload.length

    lex_fd.close()
    wet_fd.close()


if __name__ == '__main__':
  main()

