#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

"""
Global Dispatcher for the crawler

It reads the to-be-crawled items from the queue
and start worker to crawl subsequent nested pages

de-duplication will be checked before forking the workers
"""

from page_crawl import GenericPageCrawler

class Dispatcher(object):
  ''' nested crawl dispatcher '''

  def __init__(self):
    self.num_of_pages = 0
    self.bytes_of_pages = 0
    self.start()

  def start(self):

    while True:
      # get one item from the queue
      # check duplication
      # initialize a generic crawler instance
      # run that instance asyncly
      pass

