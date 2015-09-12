#!/usr/bin/env python

import unittest
from utils import DeDupeCache
from page_crawl import Page

class TestDeDupeCache(unittest.TestCase):

  def check_empty_cache(self, cache):
    self.assertTrue(cache.url_count == 0)
    self.assertTrue(cache.url_cache == {})

  def test_init_cache(self):
    ''' test DeDupeCache() class initialization '''
    cc = DeDupeCache()
    self.check_empty_cache(cc)

  def test_check_dup(self):
    ''' test de-dupe simple case with 3 URLs '''
    cc = DeDupeCache()
    self.assertFalse(cc.is_url_dup('http://www.google.com'))
    self.assertTrue(cc.url_count == 1)
    self.assertTrue(cc.is_url_dup('http://www.google.com'))
    self.assertTrue(cc.url_count == 1)

    self.assertFalse(cc.is_url_dup('http://www.nyu.edu'))
    self.assertTrue(cc.url_count == 2)
    self.assertTrue(cc.is_url_dup('http://www.nyu.edu'))
    self.assertTrue(cc.url_count == 2)

    self.assertFalse(cc.is_url_dup('http://www.nyu.edu/engineering'))
    self.assertTrue(cc.url_count == 3)
    self.assertTrue(cc.is_url_dup('http://www.nyu.edu/engineering'))
    self.assertTrue(cc.url_count == 3)

  def test_check_bulk(self):
    ''' test de-dupe with 100k URLs '''
    cc = DeDupeCache()
    
    for idx in range(100000):
      url = 'http://www.nyu.edu/engineering/access.aspx?magicnum=%d' % idx
      self.assertFalse(cc.is_url_dup(url))
      self.assertTrue(cc.url_count == idx + 1)
      self.assertTrue(cc.is_url_dup(url))
      self.assertTrue(cc.url_count == idx + 1)
      self.assertTrue(cc.is_url_dup(url))
      self.assertTrue(cc.url_count == idx + 1)

    for idx in range(100000):
      url = 'http://www.nyu.edu/engineering/access.aspx?magicnum=%d' % idx
      cc.del_url(url)
      self.assertTrue(cc.url_count == 100000 - idx - 1)

    self.check_empty_cache(cc)

