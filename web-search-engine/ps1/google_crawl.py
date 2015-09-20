#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from urlparse import urljoin
from bs4 import BeautifulSoup
import validation_check as vc

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

'''
Google Web Search Engine Crawler
'''

class GoogleWebCrawler(object):
  ''' Google Web Search Engine Crawler '''

  def __init__(self, keywords, fake):
    self.queries = keywords
    self.fake = fake

  def make_query_string(self):
    ''' make google web search query string based on keywords '''
    return "+".join(self.queries)  

  def query(self):
    ''' send google search query and get the top 10 result as a list of URLs '''

    if self.fake:
      return ['http://engineering.nyu.edu', 'http://www.nyu.edu']

    my_referer='http://www.google.com'
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
      'referer': 'http://www.google.com'
    }

    ''' send query and return list of URLs '''
    query_string = self.make_query_string()
    params = {'q':query_string}

    # make google HTTP request
    google_url = "http://www.google.com/search?"
    try:
      response = requests.get(google_url, params=params, headers = headers)

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

    # parse page contents
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    ret = []

    for link in soup.find_all('h3'):
      for linka in link.find_all('a'):
        if not linka.get('style'):
          if linka.get('href'):
            newlink = urljoin(response.url, linka.get('href'))
            retlink = vc.various_check(newlink)
            if retlink:
              ret.append(retlink)

    # return array of URls in an array
    return list(set(ret))[:10]

