#!/usr/bin/env python

import unittest
from page_crawl import Page
from page_crawl import GenericPageCrawler

class TestPageCrawl(unittest.TestCase):

  def validate_urls(self, urls):
    for url in urls:
      if not url.startswith('http'):
        return False
    return True

  def test_page_crawl(self):
    ''' test generic page crawler '''
    cr = GenericPageCrawler('http://www.nyu.edu/engineering')

if __name__ == '__main__':
  unittest.main()

