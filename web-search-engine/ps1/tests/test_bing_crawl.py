#!/usr/bin/env python

import unittest
from bing_crawl import BingWebCrawler

class TestBingCrawl(unittest.TestCase):

  def validate_urls(self, urls):
    for url in urls:
      if not url.startswith('http'):
        return False
    return True

  def test_bing_crawl_fake(self):
    ''' test bing top 10 search crawler '''
    keywords = [['new', 'york', 'university'], ['Torsten', 'Suel'], ['Amazon', 'Full', 'Time'], ['Bing', 'Ann', 'Arbor']]
    for key in keywords:
      bs = BingWebCrawler(key, fake=True)
      urls = bs.query()
      self.assertTrue(urls == ['http://engineering.nyu.edu', 'http://www.nyu.edu'])

  def test_bing_crawl(self):
    ''' test bing top 10 search crawler '''
    keywords = [['new', 'york', 'university'], ['Torsten', 'Suel'], ['Amazon', 'Full', 'Time'], ['Bing', 'Ann', 'Arbor']]
    for key in keywords:
      bs = BingWebCrawler(key, fake=False)
      urls = bs.query()
      print urls
      self.assertTrue(self.validate_urls(urls))

if __name__ == '__main__':
  unittest.main()

