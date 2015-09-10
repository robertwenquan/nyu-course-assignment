#!/usr/bin/env python

import unittest
from google_crawl import GoogleWebCrawler

class TestGoogleCrawl(unittest.TestCase):

  def validate_urls(self, urls):
    for url in urls:
      if not url.startswith('http'):
        return False
    return True

  def test_google_crawl(self):
    ''' test google top 10 search crawler '''
    gs = GoogleWebCrawler(['nyu', 'poly', 'cse'])
    urls = gs.query()
    self.assertTrue(self.validate_urls(urls))

if __name__ == '__main__':
  unittest.main()

