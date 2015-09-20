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
import md5
import math
import time
import random
import string
import validation_check as vc
''' test visited? '''
''' blacklist '''

class Page(object):
  ''' object for a crawled page '''

  def __init__(self, url, depth, score, ref=''):
    self.url = url      # page url to be crawled
    self.depth = depth  # depth of crawl, starting at 1 with google results
    self.score = score  # scores ranging [1,9], 9 is with highest priority
    self.size = 0       # page size in bytes
    self.content = ''   # page content in plaintext
    self.ref = ref      # parent page url
    self.linkhash = ''  # md5 hash of the url
    self.pagehash = ''  # md5 hash of the page content
    self.store = ''     # page store path

    self.time_start = time.time()   # crawl start timestamp
    self.time_end = -1              # crawl end timestamp
    self.time_duration = -1         # crawl time
    self.status_code = -1      # response status code

    self.update_fields()

  def update_fields(self):
    ''' update linkhash and store based on url '''
    self.linkhash = self.md5sum(self.url)
    path = urlparse(self.url).path
    if '.' in path:
      self.store = os.path.join(self.linkhash[0:2], self.linkhash[2:4], self.linkhash[4:] + '.' + path.split('.')[-1])
    else:
      self.store = os.path.join(self.linkhash[0:2], self.linkhash[2:4], self.linkhash[4:])

  def md5sum(cls, url):
    # dirty fix
    if isinstance(url, unicode):
      url = url.encode('utf-8')

    m = md5.new()
    m.update(url)
    return m.hexdigest()


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
    keywords = [word.lower() for word in self.keywords]

    #Get title and convert to lowercase
    if soup.head and soup.head.title:
      title = [ti.lower() for ti in soup.head.title.get_text().split(" ")]

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
    print self.page.url
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
    try:
      header = requests.head(self.page.url)
      if not header.headers.get('content-type'):
        return
    except requests.exceptions.RequestException as e:
      try:
        fileto = self.conf['crawl']['crawl_errs']
        dirname = os.path.dirname(fileto)
        if not os.path.exists(dirname):
          os.makedirs(dirname)

        with open(fileto, 'wb') as fpw:
          fpw.write(url, e)

      except Exception as e:
        print('Error writing back %s: %s' % (page.url, str(e)))

      return

    type = header.headers['content-type']
    if 'text/html' not in type:
      return

    #send query and get content of the current page

    try:
      response = requests.get(self.page.url, headers = headers)
    except requests.exceptions.RequestException as e:
      try:
        fileto = self.conf['crawl']['crawl_errs']
        dirname = os.path.dirname(fileto)
        if not os.path.exists(dirname):
          os.makedirs(dirname)

        with open(fileto, 'wb') as fpw:
          fpw.write(url, e)

      except Exception as e:
        print('Error writing back %s: %s' % (page.url, str(e)))

      return

    data = response.text        # data is read out as unicode
    soup = BeautifulSoup(data, 'html.parser')

    #Update page score
    self.update_page_score(soup)

    #get and return hyperlink of the current page
    self.get_next_level_page(soup)

    #send page info to log queue 
    self.page.size = len(data)
    self.page.content = data

    self.page.time_end = time.time()
    self.page.time_duration = self.page.time_end - self.page.time_start
    self.page.status_code = response.status_code

    self.log_queue.put(self.page)

  def get_next_level_page(self, soup):
    page_links = []

    for link in soup.find_all('a'):
      if not link.get('href'):
        continue
      newlink = urljoin(self.page.url, link.get('href'))
      retlink = vc.various_check(newlink)
      if retlink:
        page_links.append(retlink)

    page_links = list(set(page_links))

    for link in page_links:
      if not self.check_duplication(link):
        page = Page(link, self.page.depth + 1, self.page.score, ref=self.page.url)
        self.queue.en_queue(page)

  def check_duplication(self, link):
    return self.cache.is_url_dup(link)
