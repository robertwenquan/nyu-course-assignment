#!/usr/bin/python

import sys
import pprint
import pymongo
import argparse

class QueryMovingPath():

  def __init__(self):
    self.connMongo = None

  def conn_open(self):
    """
    open connection to MongoDB
    """

    self.connMongo = pymongo.Connection('mongodb://localhost:27017')

    db = self.connMongo.camelot
    collection = db.smartcache

    return collection

  def conn_close(self):
    """
    close the connection to MongoDB
    """

    self.connMongo.close()

  def query(self, hashid, level=3, side='south'):

    collection = self.conn_open()

    doc = collection.find_one({hashid:{"$exists": "true"}}, {"_id":0})
    item = doc[hashid]
    path = doc[hashid][str(level)][side][0]
    self.conn_close()

    return path

def main(argv):

  parser = argparse.ArgumentParser()
  parser.add_argument('-k', '--hashkey', help='hashkey of the canvass map for query', type=str)
  parser.add_argument('-s', '--side', help='side of the game', type=str)
  parser.add_argument('-l', '--level', help='difficulty level of the game', type=str)
  args = parser.parse_args()

  hashid = args.hashkey
  if hashid == None or hashid == '':
    print 'Specify HASHID to query!'
    exit(1)

  aa = QueryMovingPath()
  print aa.query(hashid, level=args.level, side=args.side)

#
# main routine starts here
#
if __name__ == '__main__':
  main(sys.argv)

