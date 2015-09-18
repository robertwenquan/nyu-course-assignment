#!/usr/bin/env python

import unittest
from google_crawl import GoogleWebCrawler

class TestGoogleCrawl(unittest.TestCase):

  def validate_urls(self, urls):
    for url in urls:
      if not url.startswith('http'):
        return False
    return True

  def test_google_crawl_fake(self):
    ''' test google top 10 search crawler '''
    keywords = [['new', 'york', 'university'], ['Torsten', 'Suel'], ['Amazon', 'Full', 'Time'], ['Google', 'Ann', 'Arbor']]
    for key in keywords:
      gs = GoogleWebCrawler(key, fake=True)
      urls = gs.query()
      self.assertTrue(urls == ['http://engineering.nyu.edu', 'http://www.nyu.edu'])

  def test_google_crawl(self):
    ''' test google top 10 search crawler '''
    keywords = [['new', 'york', 'university'], ['Torsten', 'Suel'], ['Amazon', 'Full', 'Time'], ['Google', 'Ann', 'Arbor']]
    for key in keywords:
      gs = GoogleWebCrawler(key, fake=False)
      urls = gs.query()
      self.assertTrue(self.validate_urls(urls))

if __name__ == '__main__':
  unittest.main()

