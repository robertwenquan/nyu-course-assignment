#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from utils import TaskQueue
from page_crawl import Page
from page_crawl import GenericPageCrawler
import validation_check as vc

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

    url = u'http://www.nyu.edu/engineering'
    cr = GenericPageCrawler(page, queue, None, None, keywords, fake=True)

    url = u'http://www.google.com/search?q=♥'
    cr = GenericPageCrawler(page, queue, None, None, keywords, fake=True)

  def test_normalize_url(self):
    ''' test normalize url function '''

    url = 'http://www.poly.edu/admission/page.html#tuition'
    page = Page(url, depth=1, score=9)
    queue = TaskQueue()
    keywords = ['nyu', 'poly']

    self.assertTrue(vc.normalize_link(url) == 'http://www.poly.edu/admission/page.html')

    url2 = 'http://www.poly.edu/admission/page.html#tuition#abc'
    self.assertTrue(vc.normalize_link(url2) == 'http://www.poly.edu/admission/page.html')

  def test_simplify_url(self):
    url = "http://www.poly.edu/admission/../page.html"
    page = Page(url, depth=1, score=9)
    queue = TaskQueue()
    keywords = ['nyu', 'poly']

    self.assertTrue(vc.simplify_link(url) == 'http://www.poly.edu/page.html')

    url2 = 'http://www.poly.edu/./page.html'
    self.assertTrue(vc.simplify_link(url2) == 'http://www.poly.edu/page.html')

    url3 = 'http://www.poly.edu/../../../../page.html'
    self.assertTrue(vc.simplify_link(url3) == 'http://www.poly.edu/page.html')

    url4 = 'http://www.poly.edu/aa/bb/cc/../page.html'
    self.assertTrue(vc.simplify_link(url4) == 'http://www.poly.edu/aa/bb/page.html')

    url5 = 'http://www.poly.edu/aa/bb/cc/../../../page.html'
    self.assertTrue(vc.simplify_link(url5) == 'http://www.poly.edu/page.html')

    url6 = 'http://www.poly.edu/aa/bb/cc/../../../../page.html'
    self.assertTrue(vc.simplify_link(url6) == 'http://www.poly.edu/page.html')

    url7 = 'http://www.poly.edu/./././aa/././././bb/./cc/.././././page.html'
    self.assertTrue(vc.simplify_link(url7) == 'http://www.poly.edu/aa/bb/page.html')

    url8 = [
            'http://www.poly.edu/index.html',
            'http://www.poly.edu/index.htm',
            'http://www.poly.edu/index.jsp',
            'http://www.poly.edu/index.asp',
            'http://www.poly.edu/index.aspx',
            'http://www.poly.edu/index.php',
           ]

    for url in url8:
      self.assertTrue(vc.simplify_link(url) == 'http://www.poly.edu')

    url9 = 'http://www.poly.edu/a/../../b/index.html'
    self.assertTrue(vc.simplify_link(url9) == 'http://www.poly.edu/b')

  def test_blacklist(self):
    url = "https://www.ewtn.com/library/SCRIPTUR/JOBMOST.TXT"
    self.assertTrue(vc.check_blacklist(url) == True)

    url2 = "ftp://www.google.com/"
    self.assertTrue(vc.check_blacklist(url2) == True)

    #url3 = "https://www.google.com/"
    #self.assertTrue(vc.check_blacklist(url3) == False)

  '''
  I don't now what the expected answer should be when requests failed
  def test_error_capture(self):
    url = 'https://www.ewtn.com/library/SCRIPTUR/JOBMOST.TXT'
    page = Page(url, depth=1, score=9)
    queue = TaskQueue()
    keywords = ['nyu', 'poly']
    cr = GenericPageCrawler(page, queue, None, None, keywords, fake=True)
    self.assertTrue(cr == [])
  '''
if __name__ == '__main__':
  unittest.main()
