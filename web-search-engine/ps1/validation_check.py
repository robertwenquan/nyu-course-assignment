#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
utility functions for validation check
"""

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

import urllib
import string
from urlparse import urlparse, urljoin


def various_check(link):
  norm_link = normalize_link(link)
  simple_link = simplify_link(norm_link)

  if check_blacklist(simple_link):
    return False

  return simple_link

def normalize_link(link):
  '''
  Deal with following cases:
    1. URL encoding
    2. Bookmark, which is seperate by "#"
  '''
  normlink = urllib.unquote(link)

  if '#' in normlink:
    return "".join(normlink.split('#')[0])

  return normlink

def simplify_link(link):
  urlps = urlparse(link)

  component = urlps.path.split('/')
  curpage_filename = ['index.html', 'index.htm', 'index.jsp', 'index.asp', 'index.aspx', 'index.php']

  if component[-1] in curpage_filename:
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

def check_blacklist(link):
  black_list = ['mp3','mp4','pdf','doc','jpg','png','gif','exe','txt']
  protocol_white_list = ['http', 'https']

  url = urlparse(link)

  if url.scheme not in protocol_white_list:
    return True

  path = url.path
  filename = url.path.split("/")[-1]
  extension = filename.split(".")[-1].lower()

  if extension in black_list:
    return True

  return False

def robots_disallow_check(link):
  robots = '/robots.txt'
  robot_page = urljoin(link, robots)

  try:
    r = requests.get(robot_page)

  except:
    return False

  agentname = ""
  for a in r.text.split("\n"):
    if 'user-agent' in a.lower():
      agentname = a.split(":")[-1].split(" ")[-1]
    else:
      if agentname != "*":
        continue
      aa = a.split(":")
      if aa[0].lower() == 'disallow':
        path = aa[-1]
        if path in self.page.url:
          return True
      if aa[0].lower() == 'allow':
        path = aa[-1]
        if path in self.page.url:
          return False

  return False

