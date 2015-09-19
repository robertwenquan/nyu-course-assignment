#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

"""
utility classes for local crawler mode

class TaskQueue() to simulate a priority queue
class DeDupeCache() to simulate a de-duplication hash table

"""
import urllib
import string
from urlparse import urlparse, urljoin

class ValidationCheck(object):
  def __init__(self, link):
    self.link= link

  def various_check(self):
    norm_link = self.normalize_link(self.link)
    simple_link = self.simplify_link(norm_link)

    if self.check_blacklist(simple_link):
      return False

    return simple_link 

  def normalize_link(self,link):
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
    urlps = urlparse(link)

    component = urlps.path.split('/')

    if component[-1] == 'index.html':
      del component[-1]

    while '.' in component:
      index = component.index('.')
      del component[index]

    while '..' in component:
      index = component.index('..')
      if index == 1:
        del component[index]
        continue
      del component[index]
      del component[index-1]

    path = "/".join(component)

    return link.replace(urlps.path, path)

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
