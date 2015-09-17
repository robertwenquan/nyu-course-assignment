#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

'''
Google Web Search Engine Crawler
'''

class GoogleWebCrawler(object):
  ''' Google Web Search Engine Crawler '''

  def __init__(self, keywords):
    self.queries = keywords

  def make_query_string(self):
    ''' make google web search query string based on keywords '''
    return "+".join(self.queries)  

  def query(self):
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
    response = requests.get(google_url, params=params, headers = headers)

    # parse page contents
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')

    ret = []

    for link in soup.find_all('h3'):
      for linka in link.find_all('a'):
        if not linka.get('style'):
          ret.append(linka.get('href'))

    # add this with fake mode
    #if ret == []:
    #  ret.append('http://engineering.nyu.edu')

    # return array of URls in an array
    return list(set(ret))[:10]

