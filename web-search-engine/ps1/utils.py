#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

"""
utility classes for local crawler mode

class TaskQueue() to simulate a priority queue
class DeDupeCache() to simulate a de-duplication hash table

"""

import os
import md5
import json
from page_crawl import Page

class TaskQueue(object):
  ''' global crawler task queue shared by worker and page crawler
      Input: page crawler write tasks into the queue
      Output: worker fetches the task and assigns to page crawler
  '''
  def __init__(self):
    self.prio_task_cnt = [0] * 10
    self.prio_task_list = [[]] * 10
    self.total_task_cnt = 0

  def normalize_priority(cls, score):
    return int(score * 1000) % 10

  def en_queue(self, task):
    ''' put a task into the priority queue '''
    pri = self.normalize_priority(task.score)
    assert(pri >= 0 and pri <= 9)

    self.prio_task_list[pri].append(task)
    self.prio_task_cnt[pri] += 1
    self.total_task_cnt += 1

  def de_queue(self):
    ''' get a task from the queue based on priority '''
    for pri in range(9, -1, -1):
      if self.prio_task_cnt[pri] != 0:
        self.prio_task_cnt[pri] -= 1
        self.total_task_cnt -= 1
        return self.prio_task_list[pri].pop(0)

    return None

  def flush(self):
    self.prio_task_cnt = [0] * 10
    self.prio_task_list = [[]] * 10


class DeDupeCache(object):
  ''' This is just a dictionary (hash-table) for URL deduplication
      keys are md5sum hash
  '''
  def __init__(self):
    self.url_cache = {}
    self.url_count = 0

  def md5sum(cls, url):
    m = md5.new()
    m.update(url)
    return m.hexdigest()

  def is_url_dup(self, url):
    md5sum = self.md5sum(url)
    if md5sum in self.url_cache:
      return True
    else:
      self.url_cache[md5sum] = 1
      self.url_count += 1
      return False

  def del_url(self, url):
    md5sum = self.md5sum(url)
    if md5sum in self.url_cache:
      del self.url_cache[md5sum]
      self.url_count -= 1

class Logger(object):
  ''' logger for generic logging purpose '''

  def __init__(self, logfile):
    if not os.path.exists(os.path.dirname(logfile)):
      # os.mkdir(os.path.dirname(logfile))
      return

    self.fd = open(logfile, 'a+')

  def log(self, page):
    log_entry = {'url':page.url, 'depth':page.depth, 'score':page.score, 'size':page.size, 'ref':page.ref}
    log_json_str = json.dumps(log_entry)
    self.fd.write(log_json_str + '\n')

  def close(self):
    self.fd.close()

