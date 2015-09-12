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

  def __init__(self, page, queue, cache):
    self.url = page.url
    self.depth = page.depth
    self.score = page.score

    self.queue = queue
    self.cache = cache

    self.parse()

  def parse(self):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    }
    black_list = ['mp3','mp4','pdf','doc','jpg','png','gif','exe','txt']

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
      page = Page(link, self.depth + 1, random.randint(self.score - 40, self.score - 10))
      self.queue.en_queue(page)



