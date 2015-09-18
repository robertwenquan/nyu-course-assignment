#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

'''
Generic Page Crawler and Parser
'''

import requests
from bs4 import BeautifulSoup
from urlparse import urlparse, urljoin
import urllib
import random
import os
import math
import random
import string
''' test visited? '''
''' blacklist '''

class Page(object):
  def __init__(self, url, depth, score, ref=''):
    self.url = url      # page url to be crawled
    self.depth = depth  # depth of crawl, starting at 1 with google results
    self.score = score  # scores ranging [1,9], 9 is with highest priority
    self.size = 0       # page size in bytes
    self.content = ''   # page contents in plaintext
    self.ref = ref      # parent page url

class GenericPageCrawler(object):
  ''' Generic Web Page Crawler and Parser '''

  def __init__(self, page, queue, cache, log_queue, keywords, fake):
    self.page = page

    self.queue = queue
    self.cache = cache

    self.keywords = keywords
    self.fake = fake

    self.log_queue = log_queue

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
    self.page.score /= float(3)

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
      self.page.score += 3*(key_in_title / float(len(keywords)))

      key_in_url = 0
      for word in keywords:
        if word in self.page.url:
          key_in_url += 1

      self.page.score += 3 * (key_in_url / float(len(keywords)))

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

          self.page.score += word_frequency * 200

    #Adjust it to 0 - 9
    self.page.score = int(math.ceil(self.page.score))
    if self.page.score > 9:
      self.page.score = 9

  def parse(self):
    ''' fetch the page and parse it
        1. Before fetching the page, the header of the file was fetched first
           content-type is checked. non 'text/html' MIME type will be simply ignored
        2. blacklist of file extensions are checked against the URL
        3. the page is fetched and analyzed with TF (term frequency)
        4. children links in this page are added to the crawl queue

        Note: for the fake mode
        fake mode doesn't follow any of the above process 
        but simply inject 10-20 random URLs into the queue
    '''
    # fake single page crawl starts HERE
    if self.fake:
      def gen_random_url():
        random_path = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        random_filename = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(11)) + '.html'
        random_url = urljoin('http://www.randomdomain.com/', os.path.join(random_path, random_filename))
        return random_url

      def gen_random_score():
        return random.randint(0,9)

      self.page.score = gen_random_score()
      for count in range(random.randint(10,20)):
        random_link = gen_random_url()
        page = Page(random_link, self.page.depth + 1, self.page.score, ref=self.page.url)
        self.queue.en_queue(page)

      return
    # fake single page crawl ends HERE

    # normal page crawl process starts HERE

    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    }

    #get header of url to decide whether it is crawlable
    #TODO: Deal with pages stars with "https" and so on
    urlps = urlparse(self.page.url)
    if not urlps.scheme == 'http':
      # log it
      return

    header = requests.head(self.page.url)
    if not header.headers.get('content-type'):
      return

    type = header.headers['content-type']
    if 'text/html' not in type:
      return

    #send query and get content of the current page

    response = requests.get(self.page.url, headers = headers)
    data = response.text
    soup = BeautifulSoup(data,'html.parser')

    #Update page score
    self.update_page_score(soup)

    #get and return hyperlink of the current page
    self.get_next_level_page(soup)

    #send page info to log queue 
    self.page.size = len(data)
    self.page.content = data
    self.log_queue.put(self.page)

  def get_next_level_page(self, soup):
    page_links = []

    for link in soup.find_all('a'):
      if link.get('href') and link.get('href').startswith('http'):
        page_links.append(link.get('href'))
      elif link.get('href'):
        page_links.append(urljoin(self.page.url, link.get('href')))

    page_links = list(set(page_links))

    for link in page_links:
      #Normalize
      normlink = self.normalize_link(link)

      #Simplify url
      simple_link = self.simplify_link(normlink)

      #Avoid links with undesirable extensions
      if self.check_blacklist(simple_link):
        continue

      #CHECK DEDUPLICATION
      if self.check_duplication(simple_link):
        continue

      page = Page(normlink, self.page.depth + 1, self.page.score, ref=self.page.url)
      self.queue.en_queue(page)

  def check_blacklist(self, link):
    black_list = ['mp3','mp4','pdf','doc','jpg','png','gif','exe','txt']
    protocol_black_list = ['mailto']

    url = urlparse(link)

    if url.scheme in protocol_black_list:
      return True

    path = url.path
    filename = url.path.split("/")[-1]
    extension = filename.split(".")[-1].lower()

    if extension in black_list:
      return True

    return False

  def check_duplication(self, link):
    return self.cache.is_url_dup(link)

  def normalize_link(self, link):
    '''
    Deal with following cases:
      1. URL encoding
      2. Bookmark, which is seperate by "#"
    '''
    normlink = urllib.unquote(link)

    if '#' in normlink:
      return "".join(normlink.split('#')[0]) 
    
    return normlink

  def simplify_link(self, link):
    component = link.split('/')

    while '.' in component:
      index = component.index('.')
      del component[index]

    #TODO: if '..' appeared in the component[0]
    while '..' in component:
      index = component.index('..')
      del component[index]
      del component[index-1]

    return "/".join(component)
