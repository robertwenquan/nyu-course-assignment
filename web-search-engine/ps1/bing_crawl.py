#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from urlparse import urljoin

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

'''
Google Web Search Engine Crawler
'''

class BingWebCrawler(object):
  ''' Google Web Search Engine Crawler '''

  def __init__(self, keywords, fake):
    self.queries = keywords
    self.fake = fake

  def make_query_string(self):
    ''' make bing web search query string based on keywords '''
    return "+".join(self.queries)  

  def query(self):
    ''' send google search query and get the top 10 result as a list of URLs '''

    if self.fake:
      return ['http://engineering.nyu.edu', 'http://www.nyu.edu']

    my_referer='https://www.bing.com/'
    headers = {
      'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
      'referer': my_referer
    }

    ''' send query and return list of URLs '''
    query_string = self.make_query_string()
    params = {'q':query_string}

    # make google HTTP request
    bing_url= "http://www.bing.com/search?"
    response = requests.get(bing_url, params=params, headers = headers)

    # parse page contents
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    ret = []

    for link in soup.find_all('h2'):
      for linka in link.find_all('a'):
          if linka.get('href'):
            newlink = urljoin(response.url, linka.get('href'))
            if newlink.startswith('http'):
              ret.append(newlink)

    # return array of URls in an array
    return list(set(ret))[:10]

