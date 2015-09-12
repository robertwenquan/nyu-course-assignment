#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

'''
Generic Page Crawler and Parser
'''

class Page(object):
  def __init__(self, url, depth, score):
    self.url = url
    self.depth = depth
    self.score = score

class GenericPageCrawler(object):
  ''' Generic Web Page Crawler and Parser '''

  def __init__(self, page, queue, cache):
    self.url = page.url
    self.depth = page.depth
    self.score = page.score

    self.queue = queue
    self.cache = cache

    self.parse()

  def parse(self):

    # mock up 10 sub pages and put them into the queue
    import random
    import md5

    for i in range(10):
      m = md5.new()
      m.update(str(random.randint(1000000, 6000000)))
      url = 'http://www.fakeurl.com/%s' % m.hexdigest()

      page = Page(url, self.depth + 1, random.randint(self.score - 40, self.score - 10))
      self.queue.en_queue(page)
    # end of the mock 10 pages

