#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

'''
Generic Page Crawler and Parser
'''

class Page(object):
  def __init__(self, url, depth):
    self.url = url
    self.depth = depth
    self.score = -1

class GenericPageCrawler(object):
  ''' Generic Web Page Crawler and Parser '''

  def __init__(self, url):
    self.url = url

