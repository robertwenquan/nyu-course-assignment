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
from google_crawl import GoogleWebCrawler
from crawln_dispatcher import Dispatcher

def main():
  ''' main routine function '''

  # config file reading, for keys and configurable items

  # argument parsing

  # start queue service

  # start de-duplicate hash
  # ?? here or in the dispatcher ??

  # crawl google web search engine
  gs = GoogleWebCrawler()

  # kick off dispatcher
  dp = Dispatcher()

if __name__ == '__main__':
  main()

