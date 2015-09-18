#!/usr/bin/env python

import unittest
from utils import TaskQueue
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

    url = 'http://www.nyu.edu/engineering'
    page = Page(url, depth=1, score=9)
    queue = TaskQueue()
    keywords = ['nyu', 'poly']
    cr = GenericPageCrawler(page, queue, None, keywords, fake=True)

if __name__ == '__main__':
  unittest.main()

