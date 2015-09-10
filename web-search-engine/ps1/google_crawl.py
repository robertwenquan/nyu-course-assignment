#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

'''
Google Web Search Engine Crawler
'''

class GoogleWebCrawler(object):
  ''' Google Web Search Engine Crawler '''

  def __init__(self, keywords):
    self.queries = keywords

  def make_query_string(self):
    ''' make google web search query string based on keywords '''
    pass

  def query(self):
    ''' send query and return list of URLs '''
    pass

