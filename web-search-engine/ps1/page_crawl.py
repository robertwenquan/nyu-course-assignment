#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse 
import random
''' test visited? '''
''' blacklist '''

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

'''
Generic Page Crawler and Parser
'''

class Page(object):
  def __init__(self, url, depth, score):
    self.url = url
    self.depth = depth
    self.score = score
    self.size = 0

class GenericPageCrawler(object):
  ''' Generic Web Page Crawler and Parser '''

  def __init__(self, page, queue, cache, keywords):
    self.url = page.url
    self.depth = page.depth
    self.score = page.score

    self.queue = queue
    self.cache = cache

    self.keywords = keywords

    self.parse()

  def update_page_score(self, text):
    keywords = self.keywords

    for index, item in enumerate(keywords):
      keywords[index] = keywords[index].lower()

    words = text.split(" ")

    for word in words:
      if word.lower() in keywords:
        self.score +=  10

  def parse(self):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    }

    '''get header of url to decide whether it is crawlable '''
    urlps = urlparse(self.url)
    if not urlps.scheme == 'http':
      return

    header = requests.head(self.url)
    if not header.headers.get('content-type'):
      return

    type = header.headers['content-type']
    if 'text/html' not in type:
      return

    ''' send query and return list of URLs '''

    response = requests.get(self.url, headers = headers)
    data = response.text
    soup = BeautifulSoup(data,'html.parser')

    ''' Update page score '''
    self.update_page_score(soup.get_text())

    '''Get and return links from current page'''
    return self.get_next_level_page(soup)

  def get_next_level_page(self, soup):
    black_list = ['mp3','mp4','pdf','doc','jpg','png','gif','exe','txt']
    page_links = []

    for link in soup.find_all('a'):
      if link.get('href') and link.get('href').startswith('http'):
        page_links.append(link.get('href'))

    page_links = list(set(page_links))

    for link in page_links:
      url = urlparse(link)
      path = url.path

      filename = url.path.split("/")[-1]
      extension = filename.split(".")[-1].lower()

      if extension in black_list:
        continue

      ''' CHECK DEDUPLICATION '''
      if self.check_duplication(link):
        continue

      ''' If never visited, add to queue '''
      page = Page(link, self.depth + 1, self.score/2)
      self.queue.en_queue(page)

  def check_duplication(self, link):
    return False
