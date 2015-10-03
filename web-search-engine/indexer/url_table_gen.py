#!/usr/bin/env python

"""
Scan over the WET files and generate the URL table

URL table is the table with docid mapped to crawled URL
It has the following fields:

 - docid (key)
 - url
 - wet filename
 - offset in the file
 - content start offset from the doc
 - content length

"""

import os
import glob
import warc
import random
from struct import *


WET_DIR = '/tmp/cc201507/'

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

class UrlIndex(object):

  def __init__(self):
    self.url_index_file = '/tmp/url_table.idx'
    self.url_index_urls = '/tmp/url_table.urls'
    self.url_index_offset = 0

    self.fd_urls = open(self.url_index_urls, 'wb')
    self.fd_url_idx = open(self.url_index_file, 'wb')

  def write_url_index(self, url):
    url_lens = len(url)
    fileid = 99
    offset = self.url_index_offset
    self.url_index_offset += (4 + url_lens)

    # write-back format: len(4B), url as string
    url_lens_data = pack('i', url_lens)
    self.fd_urls.write(url_lens_data)
    self.fd_urls.write(url)

    return (url_lens, fileid, offset)

  def write_url_index_entry(self, data):
    self.fd_url_idx.write(data)

def main():
  """ main routine """

  wet_files = get_wet_files()
  docid_gen = docid_generator()

  url_index = UrlIndex()

  for wet_file in wet_files:
    wet_fd = warc.open(wet_file)
    doc_next_offset = 0

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

        print docid, (url_fileid, url_offset, url_lens), (doc_fileid, doc_offset, doc_length, content_offset, content_length)

        # docid(4B), url_pos[fileid(2B), offset(4B), lens(2B)], doc_pos[fileid(2B), offset(4B), lens(4B), con_offset(2B), con_lens(4B)]
        url_idx_data = pack('ihihhiihi', docid, url_fileid, url_offset, url_lens, doc_fileid, doc_offset, doc_length, content_offset, content_length)
        url_index.write_url_index_entry(url_idx_data)

        doc_next_offset = wet_record.payload.fileobj.tell() + wet_record.payload.length

if __name__ == '__main__':
  main()

