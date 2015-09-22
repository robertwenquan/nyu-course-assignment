#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
utility classes for local crawler mode

class TaskQueue() to simulate a priority queue
class DeDupeCache() to simulate a de-duplication hash table

"""

__author__ = "Robert Wen <robert.wen@nyu.edu>, Caicai Chen <caicai.chen@nyu.edu>"

import os
import md5
import json
import Queue
import threading
import time


class TaskQueue(object):
  ''' global crawler task queue shared by worker and page crawler
      Input: page crawler write tasks into the queue
      Output: worker fetches the task and assigns to page crawler
  '''
  def __init__(self):
    self.prio_task_cnt = [0] * 10
    self.prio_task_list = [[]] * 10
    self.total_task_cnt = 0

  def normalize_priority(self, score):
    return int(score * 1000) % 10

  def en_queue(self, task):
    ''' put a task into the priority queue '''

    # set enqueue time
    task.time_enqueue = time.time()

    pri = self.normalize_priority(task.score)

    self.prio_task_list[pri].append(task)
    self.prio_task_cnt[pri] += 1
    self.total_task_cnt += 1

  def de_queue(self):
    ''' get a task from the queue based on priority '''

    for pri in range(9, -1, -1):
      if self.prio_task_cnt[pri] != 0:
        self.prio_task_cnt[pri] -= 1
        self.total_task_cnt -= 1

        page = self.prio_task_list[pri].pop(0)
        page.time_dequeue = time.time()
        page.queue_duration = page.time_dequeue - page.time_enqueue
        return page

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

  def md5sum(self, url):
    # dirty fix
    if isinstance(url, unicode):
      url = url.encode('utf-8')

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

    self.fdlog = open(logfile, 'a+')

  def log(self, page):
    log_entry = {'url':page.url, 'depth':page.depth, 'score':page.score, 'size':page.size,
                 'ref':page.ref, 'store':page.store, 'linkhash':page.linkhash,
                 'start':time.ctime(page.time_start), 'time':page.time_duration,
                 'enqueue':time.ctime(page.time_enqueue), 'time_in_q':page.queue_duration,
                 'code':page.status_code
                }
    log_json_str = json.dumps(log_entry)
    self.fdlog.write(log_json_str + '\n')

  def close(self):
    self.fdlog.close()


class Worker(object):

  ''' Worker thread for concurrent process of tasks from a queue using multiple threads.
      This worker is designed to never die, always keeping num_threads threads active.
      It can work on any function with arbitrary arguemtns using the add_task() method.

  Example:
    worker = Worker(50)
    for i in xrange(100):
      worker.add_task(func, arg1, arg2)  # blocks when queue is full
    worker.join()  # blocks here

  Args:
    num_threads: the number of num_threads threads to use from the Queue.
    queue_size: the number of elements that can be placed in Queue. If 0 then infinite.
  '''

  def __init__(self, num_threads=1, queue_size=0, keep_alive=True, quiet=False):
    if queue_size != 0 and queue_size < num_threads:
      raise Exception('queue_size has to be > num_threads to make sense')
    self.num_threads = num_threads
    self.queue = Queue.Queue(queue_size)
    self.threads = []
    self.keep_alive = keep_alive
    self.quiet = quiet
    self._retain_threads()  # Start the threads.
    # The following extra thread keeps all the threads alive even if they are crashing.
    # This makes it possible to block on a queue size, have threads fail, and still be able to add
    # more to the queue because this thread will spawn more new ones to take some stuff off the
    # queue.
    self.thr = threading.Thread(target=self._keep_alive, args=[self])
    self.thr.setDaemon(True)
    self.thr.start()

  def _retain_threads(self):
    ''' Make sure there at self.num_threads always. '''

    while len(self.threads) < self.num_threads:
      t = threading.Thread(target=self._run, args=[self])
      t.setDaemon(True)
      t.start()
      self.threads.append(t)

  def _keep_alive(self, *args):
    ''' This is called by thread self.t to keep all the self.threads alive forever. '''

    while self.keep_alive:
      # This join(1) here checks if the thread hit an exception and terminated
      self.threads = [t.join(1) or t for t in self.threads if t.isAlive()]
      if not self.queue.empty() and self.keep_alive:
        self._retain_threads()

  def _end_func(self):
    ''' Dummy function that when added it stops the threads. '''

    pass

  def _run(self, *args):
    ''' This is the function the threads have as their targets. '''

    while True:
      (func, args, kargs) = self.queue.get()
      if func == self._end_func:  # Check for dummy function and if so end thread.
        break
      func(*args, **kargs)

  def restart(self):
    ''' If the threads have been killed by a KeyboardInterrupt, then you can call this on the worker
    to set keep_alive to True and recreate the extra thread which in turn creates worker threads.
    '''

    self.keep_alive = True
    self._retain_threads()
    del self.thr
    self.thr = threading.Thread(target=self._keep_alive, args=[self])
    self.thr.setDaemon(True)
    self.thr.start()

  def apply_async(self, func, args):  # to match multiprocessing.ThreadPool
    self.add_task(func, *args)

  def add_task(self, func, *args, **kargs):
    ''' Add a task to the queue, blocking if the queue is full. This also resets the threads to do
    work.
    '''

    if not self.threads:
      self.restart()
    self.queue.put((func, args, kargs))

  def close(self):  # to match multiprocessing.ThreadPool
    pass

  def join(self, block=True, timeout=None):
    ''' Wait for the queue to empty.
    Args:
      block: If block is True, this will stall the interpreter at that line until the queue is
    empty, recreating threads if they die until the queue is empty. If False, this just recreates
    any stalled threads once, and returns so the interpreter can go on. Setting to False does not
    ensure that threads will stay alive, but is handy to keep more tasks to work on until you
    finally want to wait on all them to be finished at the end of your program.
    '''

    if timeout is not None:
      start_time = time.time()
      time_join = timeout
    else:
      time_join = 100
    if block:
      try:
        # Keep the threads going until the queue is emptied.
        # This is the marker to to the threads, so put it in the queue now.
        for t in range(self.num_threads):
          self.add_task(self._end_func)
        while self.threads and (timeout is None or time.time() - start_time < timeout):
          if self.queue.empty():
            raise Exception()
          time.sleep(0.0001)
      except KeyboardInterrupt:
        # self.threads = [t.join(0.01 / self.num_threads) or t for t in self.threads if t.isAlive()]
        self.keep_alive = False
        for t in range(self.num_threads):
          self.add_task(self._end_func)
      except Exception:
        # Prevent the keep_alive thread from running
        self.keep_alive = False
        # Stop all the work threads.
        for t in range(self.num_threads):
          self.add_task(self._end_func)
        # Wait on threads.
        self.threads = [t.join(time_join) or t for t in self.threads if t.isAlive()]

