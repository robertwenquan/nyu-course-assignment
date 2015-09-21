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
import sys
import time
import threading
import Queue
from utils import Logger
from utils import Worker
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

    self.crawl_in_progress = 0

    self.crawled_pages = 0
    self.crawled_bytes = 0

    self.crawled_succ = 0
    self.crawled_fail = 0

    self.crawled_page_per_sec = -1
    self.crawled_byte_per_sec = -1
    self.crawled_succ_rate = -1

  def update_crawl_bytes(self, nbyte):
    ''' increase crawled bytes '''
    self.crawled_bytes += nbyte

  def update_crawl_count(self, npage, success=True):
    ''' increase crawled pages '''
    self.crawled_pages += npage

    if success:
      self.crawled_succ += npage
    else:
      self.crawled_fail += npage

  def finalize(self):
    ''' mark the crawl end time
        and calculate crawl rate by page and byte
    '''
    self.crawl_end_time = time.time()

    duration = self.crawl_end_time - self.crawl_start_time
    self.crawled_page_per_sec = self.crawled_pages / duration
    self.crawled_byte_per_sec = self.crawled_bytes / duration
    self.crawled_succ_rate = int(self.crawled_succ) / float(self.crawled_pages)

    # write back statistics
    with open(self.crawl_stats_file, 'w') as fdw:
      self.write_crawl_stats(fdw)

  def write_crawl_stats(self, fdw):
    ''' write back crawl statistics
      - number of pages crawled
      - size of bytes crawled
      - crawl start time
      - crawl end time
      - crawl speed page per sec
      - crawl speed bytes per sec
    '''

    duration = self.crawl_end_time - self.crawl_start_time

    print('Crawl   start: ' + time.ctime(self.crawl_start_time), file=fdw)
    print('Crawl    stop: ' + time.ctime(self.crawl_end_time), file=fdw)
    print('Crawl    time: %.1f secs' % duration, file=fdw)
    print('Crawled pages: %15d (%.1f pages / sec)' %
          (self.crawled_pages, self.crawled_page_per_sec), file=fdw)
    print('Crawled bytes: %15d (%d bytes / sec)' %
          (self.crawled_bytes, self.crawled_byte_per_sec), file=fdw)
    print('Crawled success rate: %.2f' % self.crawled_succ_rate, file=fdw)


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

    # shutdown signal
    self.shutdown = False

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

  def call_crawl_page(self, page):
    ''' thread function to be called '''
    GenericPageCrawler(page, self.queue, self.cache, self.log_queue, self.keywords, self.args.fake)

  def run_page_crawler(self):
    ''' listen to crawler priority queue and crawl pages '''

    worker = Worker(50)
    while True:
      # get one item from the queue
      # initialize a generic crawler instance
      page = self.queue.de_queue()
      if page:
        self.stats.crawl_in_progress += 1
        page.time_dequeue = time.time()
        worker.add_task(self.call_crawl_page, page)

      if self.stats.crawl_in_progress == self.max_num_pages:
        break

    worker.join()
    self.shutdown = True
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
        self.stats.update_crawl_bytes(page_size)
        self.store_page(page)
        self.logger.log(page)

        if page.error == 1:
          self.stats.update_crawl_count(1, success=False)
        else:
          self.stats.update_crawl_count(1, success=True)

      if page == page_end:
        break

  def run_progress_reporter(self):
    ''' report crawling progress every N seconds
        N is based on configuration or
          argument -i (interval)

        reporting metrics include:
        - # of pages crawled.
        - successful rate.
        - # % finished.
        - # pages / sec
        - # bytes / sec
    '''

    # generate current progress report
    def progress_report_current():
      crawl_total = self.max_num_pages
      crawled_pages = self.stats.crawled_pages
      progress = '%d/%d pages crawled. [%d%%] finished' % (crawled_pages, crawl_total, (100*crawled_pages/crawl_total))
      return progress

    # generate current progress report END

    try:
      interval = self.conf['report']['interval']
    except:
      interval = 3

    while True:
      print(time.ctime() + '\t' +  progress_report_current())
      time.sleep(interval)

      if self.shutdown:
        break

    # print finish statistics
    print(time.ctime() + '\t' +  progress_report_current())
    print('')
    self.stats.write_crawl_stats(sys.stdout)
    print('crawl finished.')

  def run(self):
    ''' run the dispatcher '''

    # crawl google web search engine
    gs = GoogleWebCrawler(self.keywords, self.args.fake)

    urls = gs.query()
    if not urls and gs.error > 0:
      print('Network Error. Please check network connection.')
      return

    if not urls:
      bs = BingWebCrawler(self.keywords, self.args.fake)
      urls = bs.query()

    if not urls:
      print('See crawl failed. Please check network connection or contact the author.')
      return

    self.bulk_url_enqueue(urls)

    # launch the crawler thread
    t_crawler = threading.Thread(target=self.run_page_crawler)
    t_crawler.daemon = True
    t_crawler.start()

    # launch the log writer thread
    t_logger = threading.Thread(target=self.run_log_writter)
    t_logger.daemon = True
    t_logger.start()

    # launch the progress reporter
    t_reporter = threading.Thread(target=self.run_progress_reporter)
    t_reporter.daemon = True
    t_reporter.start()

    # wait for the workers to finish
    t_crawler.join()
    t_logger.join()

    # finalize statistical metrics
    self.stats.finalize()

    # close reporter
    t_reporter.join()

    # close logger
    self.logger.close()

