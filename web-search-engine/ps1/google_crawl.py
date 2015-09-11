#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError

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
    pass

  def query(self):
    ''' send query and return list of URLs '''
    query_string = self.make_query_string()

    # make google HTTP request
    google_url = "http://www.google.com/search?"
    params = {'q':query_string}
    response = requests.get(google_url, params=params)

    # parse page contents
    file = open('mainpage.xml', 'w')
    file.write(response.text)
    file.close()

    #tree = ET.parse('mainpage.xml')
    #root = tree.getroot()
    


    # return array of URls in an array

    return ['http://www.aaa.com', 'http://www.bbb.com']

