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
from utils import TaskQueue
from utils import DeDupeCache
from crawln_dispatcher import Dispatcher

def main():
  ''' main routine function '''

  # config file reading, for keys and configurable items

  # argument parsing
  keywords = ['nyu', 'poly', 'computer science']

  # start queue service
  qs = TaskQueue()

  # start de-duplicate hash
  cc = DeDupeCache()

  # kick off dispatcher
  dp = Dispatcher(qs, cc, keywords)

if __name__ == '__main__':
  main()

