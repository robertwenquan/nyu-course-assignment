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

  def test_page_crawler_init(self):
    ''' test generic page crawler initialization '''

    url = 'http://www.nyu.edu/engineering'
    page = Page(url, depth=1, score=9)
    queue = TaskQueue()
    keywords = ['nyu', 'poly']
    cr = GenericPageCrawler(page, queue, None, None, keywords, fake=True)

  def test_normalize_url(self):
    ''' test normalize url function '''

    url = 'http://www.poly.edu/admission/page.html#tuition'
    page = Page(url, depth=1, score=9)
    queue = TaskQueue()
    keywords = ['nyu', 'poly']
    cr = GenericPageCrawler(page, queue, None, None, keywords, fake=True)

    self.assertTrue(cr.normalize_link(url) == 'http://www.poly.edu/admission/page.html')

    url2 = 'http://www.poly.edu/admission/page.html#tuition#abc'
    self.assertTrue(cr.normalize_link(url2) == 'http://www.poly.edu/admission/page.html')

if __name__ == '__main__':
  unittest.main()

