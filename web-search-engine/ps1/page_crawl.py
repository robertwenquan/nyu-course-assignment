#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse 
import random
import math
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

  def update_page_score(self, soup):
    '''
    Get score of a page according to following three parts:
      1. Whether "title" contains keywords
      2. Whether "URL" contains keywords
      3. Frequency of keywords appeared in content
      4. Degree of mixing of keywords in content, represented by entropy
    '''

    #Inherit 1/3 of its parent page score
    self.score /= float(3)

    #Lower case of keywords
    keywords = map(lambda word: word.lower(), self.keywords)

    #Get title and convert to lowercase
    if soup.head and soup.head.title:
      title = map(lambda word: word.lower(), soup.head.title.get_text().split(" "))

      #See if title contains key word
      key_in_title = 0
      for word in keywords:
        if word in title:
          key_in_title += 1

      #Ratio of keywords contains in URL
      self.score += 3*(key_in_title / float(len(keywords)))

      key_in_url = 0
      for word in keywords:
        if word in self.url:
          key_in_url += 1

      self.score += 3 * (key_in_url / float(len(keywords)))

    #Keyword in content
    if soup.body:
      body = soup.body.get_text().split(" ")
      if len(body) != 0:
        body = map(lambda word: word.lower(), body)

        key_in_content = 0
        for word in keywords:
          key_in_content += body.count(word)

        if key_in_content != 0:
          #Calculate entropy of keywords
          entropy = 0.5

          for key in keywords:
            entropy -= math.log(((body.count(key)+1)/ float(key_in_content)))/len(keywords)

          word_frequency = key_in_content * entropy / len(body)

          self.score += word_frequency * 200

    #Adjust it to 0 - 9
    self.score = math.ceil(self.score)
    if self.score > 9:
      self.score = 9

  def parse(self):
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    }

    #get header of url to decide whether it is crawlable
    urlps = urlparse(self.url)
    if not urlps.scheme == 'http':
      return

    header = requests.head(self.url)
    if not header.headers.get('content-type'):
      return

    type = header.headers['content-type']
    if 'text/html' not in type:
      return

    #send query and get content of the current page

    response = requests.get(self.url, headers = headers)
    data = response.text
    soup = BeautifulSoup(data,'html.parser')

    #Update page score
    self.update_page_score(soup)

    #get and return hyperlink of the current page
    self.get_next_level_page(soup)

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

      #CHECK DEDUPLICATION
      if self.check_duplication(link):
        continue

      #If the current page never visited, add to queue
      page = Page(link, self.depth + 1, self.score)
      self.queue.en_queue(page)

  def check_duplication(self, link):
    return False
