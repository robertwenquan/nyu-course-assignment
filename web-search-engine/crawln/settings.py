#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
global settings for the crawler
This includes the passed in arguments and the file based config items
"""

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

import yaml
import argparse

class Settings(object):
  ''' config for the crawln crawler '''

  def __init__(self):
    self.args = None
    self.conf = None

    # config file parsing
    self.cfg_parse()

    # argument parsing
    self.arg_parse()

  def arg_parse(self):
    ''' parse command line arguments '''

    # build the arg parser
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', nargs='?', type=int, help='number of pages to crawl',
                        default=10)
    parser.add_argument('--fake', action='store_true', help='fake run, do not crawl')
    parser.add_argument('-i', '--interval', type=int, help='progress reporting interval')
    parser.add_argument('-t', '--thread', type=int, help='number of concurrent page crawlers', default=50)
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output for debugging')
    parser.add_argument('keywords', metavar='keyword', type=str, nargs='*',
                        help='keyword to search', default=['nyu', 'poly'])

    # parse arguments
    self.args = parser.parse_args()

    # override configurations from arguments
    if self.args.interval:
      self.conf['report']['interval'] = self.args.interval

  def cfg_parse(self):
    ''' parse yaml configuration file '''

    conf_file = 'crawln.yml'
    with open(conf_file, 'r') as fdr:
      data = fdr.read()

    try:
      self.conf = yaml.load(data)
    except Exception as e:
      print 'parsing crawln.yml config file failed: %s' % str(e)
      exit(2)

