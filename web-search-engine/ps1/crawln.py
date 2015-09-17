#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
crawln.py: crawler for N pages starting from Google Search Engine

How to run:
$ python crawln.py [-n [NUM]] [keyword [keyword ...]]

Default with search 'nyu poly' with 10 pages
$ python crawln.py

The following launch will search 'nyu poly computer science' and crawl 1000 pages
$ python crawln.py -n 1000 'nyu poly computer science'

Input: keyword(s), number of pages to crawl
Output: pages in organized directory and statistics

How does it work?
  send google search query
  read queue as a loop, exit when the queue has been empty for 30s or crawled item reached N
"""

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

from utils import TaskQueue
from utils import DeDupeCache
from crawln_dispatcher import Dispatcher
from settings import Settings

def main():
  ''' main routine function '''

  # argument passing and config file reading
  st = Settings()

  # start queue service
  qs = TaskQueue()

  # start de-duplicate hash
  cc = DeDupeCache()

  # kick off dispatcher
  Dispatcher(qs, cc, st)


if __name__ == '__main__':
  main()

