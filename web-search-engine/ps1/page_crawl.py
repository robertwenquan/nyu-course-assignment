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
    my_referer='http://www.google.com'

    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
      'referer': 'http://www.google.com'
    }

    ''' send query and return list of URLs '''

    response = requests.get(self.url, headers = headers)
    data = response.text
    soup = BeautifulSoup(data,'html.parser')
    black_list = ['mp3','mp4','pdf','doc','jpg','png','gif','exe','txt']
    white_list = ['html', 'htm', 'shtml', 'php', 'jsp', 'asp', 'aspx']


    page_links = []

    for link in soup.find_all('a'):
      if link.get('href') and link.get('href').startswith('http'):
        page_links.append(link.get('href'))

    page_links = list(set(page_links))

    for link in page_links:
      url = urlparse(link)
      path = url.path

      i = len(url.path) - 1  
      while i > 0:  
        if url.path[i] == '/':  
          break  
        i = i - 1  

      filename = url.path[i+1:len(url.path)]
      extension = filename.split(".")[-1]

      if extension in black_list:
        continue
      if extension in white_list:
        page = Page(link, self.depth + 1, random.randint(self.score - 40, self.score - 10))
        self.queue.en_queue(page)
      else:
        if not url.scheme == 'http':
          continue
        header = requests.head(link)
        if header.headers.get('content-type'):
          type = header.headers['content-type']
          if 'text/html' in type:
            page = Page(link, self.depth + 1, random.randint(self.score - 40, self.score - 10))
            self.queue.en_queue(page)



