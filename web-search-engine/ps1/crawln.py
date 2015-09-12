#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

"""
crawln.py: crawler for N pages starting from Google Search Engine

How to run: 
$ python crawln.py [-n 1000] cat dog animal

Input: keyword(s), number of pages to crawl
Output: pages in organized directory and statistics

How does it work?
  send google search query
  read queue as a loop, exit when the queue has been empty for 30s or crawled item reached N
"""

import argparse

from utils import TaskQueue
from utils import DeDupeCache
from crawln_dispatcher import Dispatcher

def arg_parse():
  parser = argparse.ArgumentParser('web cralwer for N pages')
  parser.add_argument('-n', '--num', nargs='?', type=int, help='number of pages to crawl', default = 1000)
  parser.add_argument('keywords', metavar='keyword', type=str, nargs='+', help='keyword to search')
  args = parser.parse_args()

  return args.keywords, args.num
  
def main():
  ''' main routine function '''

  # config file reading, for keys and configurable items

  # argument parsing
  keywords, max_num_pages = arg_parse()

  # start queue service
  qs = TaskQueue()

  # start de-duplicate hash
  cc = DeDupeCache()

  # kick off dispatcher
  dp = Dispatcher(qs, cc, keywords, max_num_pages)


if __name__ == '__main__':
  main()

