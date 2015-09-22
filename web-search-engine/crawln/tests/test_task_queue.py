#!/usr/bin/env python

import unittest
from utils import TaskQueue
from page_crawl import Page

class TestTaskPriorityQueue(unittest.TestCase):

  def check_empty_queue(self, queue):
    self.assertTrue(queue.total_task_cnt == 0)

    for pri in range(10):
      self.assertTrue(queue.prio_task_cnt[pri] == 0)
      self.assertTrue(queue.prio_task_list[pri] == [])

  def test_init(self):
    q = TaskQueue()
    self.check_empty_queue(q)

  def test_simple_enqueue_dequeue(self):
    q = TaskQueue()
    task = Page('http://www.google.com', 1, 80)
    q.en_queue(task)

    self.assertTrue(q.total_task_cnt == 1)
    self.assertTrue(q.prio_task_cnt[0] == 1)
    self.assertTrue(q.prio_task_list[0] == [task])

    outtask = q.de_queue()
    self.assertTrue(outtask.depth == 1)
    self.assertTrue(outtask.score == 80)
    self.assertTrue(outtask.url == 'http://www.google.com')

    self.check_empty_queue(q)

  def test_bulk_enqueue_dequeue(self):
    q = TaskQueue()

    for cnt in range(10000):
      task = Page('http://www.nyu.edu/engineering', 2, 60)
      q.en_queue(task)

    self.assertTrue(q.total_task_cnt == 10000)
    self.assertTrue(q.prio_task_cnt[0] == 10000)
    self.assertTrue(len(q.prio_task_list[0]) == 10000)

    while 1:
      outtask = q.de_queue()
      if not outtask:
        break

      self.assertTrue(outtask.url == 'http://www.nyu.edu/engineering')
      self.assertTrue(outtask.depth == 2)
      self.assertTrue(outtask.score == 60)

    self.check_empty_queue(q)

if __name__ == '__main__':
  unittest.main()

