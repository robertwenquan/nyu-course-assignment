#!/usr/bin/env python

import unittest
from utils import TaskQueue
from page_crawl import Page
from page_crawl import GenericPageCrawler
from validation_check import ValidationCheck

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
    vc = ValidationCheck(url)

  def test_normalize_url(self):
    ''' test normalize url function '''

    url = 'http://www.poly.edu/admission/page.html#tuition'
    page = Page(url, depth=1, score=9)
    queue = TaskQueue()
    keywords = ['nyu', 'poly']
    vc = ValidationCheck(url)

    self.assertTrue(vc.normalize_link(url) == 'http://www.poly.edu/admission/page.html')

    url2 = 'http://www.poly.edu/admission/page.html#tuition#abc'
    self.assertTrue(vc.normalize_link(url2) == 'http://www.poly.edu/admission/page.html')

  def test_simplify_url(self):
    url = "http://www.poly.edu/admission/../page.html"
    page = Page(url, depth=1, score=9)
    queue = TaskQueue()
    keywords = ['nyu', 'poly']
    vc = ValidationCheck(url)

    self.assertTrue(vc.simplify_link(url) == 'http://www.poly.edu/page.html')

    url2 = 'http://www.poly.edu/./page.html'
    self.assertTrue(vc.simplify_link(url2) == 'http://www.poly.edu/page.html')

    url3 = 'http://www.poly.edu/../../../../page.html'
    self.assertTrue(vc.simplify_link(url3) == 'http://www.poly.edu/page.html')

if __name__ == '__main__':
  unittest.main()

