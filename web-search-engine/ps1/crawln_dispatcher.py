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


import os
import time
import threading
import Queue
from utils import Logger
from page_crawl import GenericPageCrawler
from page_crawl import Page
from google_crawl import GoogleWebCrawler
from bing_crawl import BingWebCrawler


class CrawlStats(object):
  ''' statistical metrics for the crawler '''

  def __init__(self, filename):

    self.crawl_stats_file = filename

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

    with open(self.crawl_stats_file, 'w') as fdw:
      print('Crawl   start: ' + time.ctime(self.crawl_start_time), file=fdw)
      print('Crawl    stop: ' + time.ctime(self.crawl_end_time), file=fdw)
      print('Crawl    time: %.1f secs' % duration, file=fdw)
      print('Crawled pages: %15d (%.1f pages / sec)' %
            (self.crawled_pages, self.crawled_page_per_sec), file=fdw)
      print('Crawled bytes: %15d (%d bytes / sec)' %
            (self.crawled_bytes, self.crawled_byte_per_sec), file=fdw)


class Dispatcher(object):
  ''' nested crawl dispatcher '''

  def __init__(self, queue, cache, st):
    self.queue = queue
    self.cache = cache
    self.keywords = st.args.keywords
    self.args = st.args
    self.conf = st.conf

    self.num_of_pages = 0
    self.bytes_of_pages = 0

    self.max_num_pages = st.args.num

    self.logger = Logger(self.conf['crawl']['crawl_log'])
    self.stats = CrawlStats(self.conf['crawl']['crawl_stats'])

    self.log_queue = Queue.Queue()
    self.end_page_log_item = Page('none', 0, 0)

  def bulk_url_enqueue(self, urls):
    ''' add a list of URLs into the crawl queue '''
    for url in urls:
      page = Page(url, depth=1, score=9)
      self.queue.en_queue(page)

  def store_page(self, page):
    ''' store cralwed page into persistent store '''

    try:
      fileto = os.path.join(self.conf['crawl']['crawl_pages'], page.store)
      dirname = os.path.dirname(fileto)
      if not os.path.exists(dirname):
        os.makedirs(dirname)

      with open(fileto, 'wb') as fpw:
        fpw.write(page.content.encode('utf-8'))
    except Exception as e:
      print('Error writing back %s: %s' % (page.url, str(e)))

  def run_page_crawler(self):
    ''' listen to crawler priority queue and crawl pages '''

    while True:
      # get one item from the queue
      # initialize a generic crawler instance
      page = self.queue.de_queue()
      if page:
        GenericPageCrawler(page, self.queue, self.cache, self.log_queue, self.keywords, self.args.fake)

      if self.stats.crawled_pages == self.max_num_pages:
        break

    self.log_queue.put(self.end_page_log_item)

  def run_log_writter(self):
    ''' listen to log FIFO queue and write back crawl logs '''

    page_end = self.end_page_log_item

    while True:
      # get one log item from the queue
      # 1. write back crawl page meta info including page link, size, depth, score, etc.
      # 2. write crawled page back to the persistent storage
      page = self.log_queue.get()
      if page and page != page_end:
        page_size = page.size
        self.stats.update_page_info(1, page_size)
        self.store_page(page)
        self.logger.log(page)

      if page == page_end:
        break

  def run(self):
    ''' run the dispatcher '''

    # crawl google web search engine
    gs = GoogleWebCrawler(self.keywords, self.args.fake)

    urls = gs.query()

    if not urls:
      bs = BingWebCrawler(self.keywords, self.args.fake)
      urls = bs.query()

    self.bulk_url_enqueue(urls)

    # launch the crawler thread
    t_crawler = threading.Thread(target=self.run_page_crawler)
    t_crawler.daemon = True
    t_crawler.start()

    # launch the log writer thread
    t_logger = threading.Thread(target=self.run_log_writter)
    t_logger.daemon = True
    t_logger.start()

    # wait for the workers to finish
    t_crawler.join()
    t_logger.join()

    # finalize statistical metrics
    self.stats.finalize()

    # close logger
    self.logger.close()

