#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Global Dispatcher for the crawler

It reads the to-be-crawled items from the queue
and start worker to crawl subsequent nested pages

de-duplication will be checked before forking the workers
"""

from __future__ import print_function

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"


import time
from utils import Logger
from page_crawl import GenericPageCrawler
from page_crawl import Page
from google_crawl import GoogleWebCrawler


class CrawlStats(object):
  ''' statistical metrics for the crawler '''

  def __init__(self):
    self.crawl_start_time = time.time()
    self.crawl_end_time = -1

    self.crawled_pages = 0
    self.crawled_bytes = 0

    self.crawled_page_per_sec = -1
    self.crawled_byte_per_sec = -1

  def update_page_info(self, npage, nbyte):
    ''' increase crawled pages and bytes '''
    self.crawled_pages += npage
    self.crawled_bytes += nbyte

  def finalize(self):
    ''' mark the crawl end time
        and calculate crawl rate by page and byte
    '''
    self.crawl_end_time = time.time()

    duration = self.crawl_end_time - self.crawl_start_time
    self.crawled_page_per_sec = self.crawled_pages / duration
    self.crawled_byte_per_sec = self.crawled_bytes / duration

    # write back statistics
    self.write_crawl_stats()

  def write_crawl_stats(self):
    ''' write back crawl statistics
      - number of pages crawled
      - size of bytes crawled
      - crawl start time
      - crawl end time
      - crawl speed page per sec
      - crawl speed bytes per sec
    '''

    duration = self.crawl_end_time - self.crawl_start_time

    fileto = '/tmp/crawl.stats'
    fdw = open(fileto, 'w')
    print('Crawl   start: ' + time.ctime(self.crawl_start_time), file=fdw)
    print('Crawl    stop: ' + time.ctime(self.crawl_end_time), file=fdw)
    print('Crawl    time: %.1f secs' % duration, file=fdw)
    print('Crawled pages: %15d (%.1f pages / sec)' %
          (self.crawled_pages, self.crawled_page_per_sec), file=fdw)
    print('Crawled bytes: %15d (%d bytes / sec)' %
          (self.crawled_bytes, self.crawled_byte_per_sec), file=fdw)
    fdw.close()

class Dispatcher(object):
  ''' nested crawl dispatcher '''

  def __init__(self, queue, cache, st):
    self.queue = queue
    self.cache = cache
    self.keywords = st.args.keywords
    self.args = st.args

    self.logger = Logger('/tmp/crawl.log')

    self.num_of_pages = 0
    self.bytes_of_pages = 0

    self.max_num_pages = st.args.num

    self.stats = CrawlStats()

  def bulk_url_enqueue(self, urls):
    ''' add a list of URLs into the crawl queue '''
    for url in urls:
      page = Page(url, depth=1, score=9)
      self.queue.en_queue(page)

  def run(self):
    ''' run the dispatcher '''

    # crawl google web search engine
    gs = GoogleWebCrawler(self.keywords, self.args.fake)

    urls = gs.query()
    self.bulk_url_enqueue(urls)

    while True:
      # get one item from the queue
      # check duplication
      # initialize a generic crawler instance
      # run that instance asyncly
      page = self.queue.de_queue()
      if page:
        GenericPageCrawler(page, self.queue, self.cache, self.keywords, self.args.fake)
        self.stats.update_page_info(1, 1223)
        self.logger.log(page)

      if self.stats.crawled_pages == self.max_num_pages:
        break

    # finalize statistical metrics
    self.stats.finalize()

    # close logger
    self.logger.close()

