"""
the main classes for the crawler and trainer
"""

import argparse

class Crawler(object):

  def __init__(self, keyword):
    self.keyword = keyword

class TextCrawler(Crawler):
  pass

class ImageCrawler(Crawler):
  pass

class SocialMediaCrawler(Crawler):
  pass 

class IterativeTrainer(object):

  def __init__(self, keyword):
    self.keyword = keyword

  def run(self):
    pass

  def seed_crawl(self):
    pass

  def crawl(self):
    pass

  def train(self):
    pass

  def report(self):
    pass
  

def main():
  """ entry of the program """
  print "start the trainer."

  parser = argparse.ArgumentParser()

  # setup the trainer
  itrainer = IterativeTrainer("apple")

  # run the trainer
  itrainer.run()

  # report the metrics
  itrainer.report()


if __name__ == '__main__':
  main()

