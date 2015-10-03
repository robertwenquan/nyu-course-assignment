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


WET_DIR = '/tmp/cc201507/'

def get_wet_files():
  """ get a list of wet full path filenames """
  glob_path = os.path.join(WET_DIR, '*.wet')
  return glob.glob(glob_path)

def main():
  """ main routine """

  wet_files = get_wet_files()

  for wet_file in wet_files:
    wet_fd = warc.open(wet_file)
    for wet_record in wet_fd:
      if wet_record.url:
        print wet_record.url


if __name__ == '__main__':
  main()

