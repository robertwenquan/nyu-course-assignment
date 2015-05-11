#!/usr/bin/python

import sys
import pprint
import pymongo
import argparse

class QueryMovingPath():

  def __init__(self):
    self.connMongo = None

  # Open the MongoDB connection
  def conn_open(self):

    self.connMongo = pymongo.Connection('mongodb://localhost:27017')

    db = self.connMongo.camelot
    collection = db.smartcache

    return collection

  # Close the MongoDB connection
  def conn_close(self):
    self.connMongo.close()

  def query(self, hashid):

    collection = self.conn_open()

    doc = collection.find_one({hashid:{"$exists": "true"}}, {"_id":0})
    pprint.pprint(doc)

    self.conn_close()

def main(argv):

  parser = argparse.ArgumentParser()
  parser.add_argument('-k', '--hashkey', help='hashkey of the canvass map for query', type=str)
  args = parser.parse_args()

  hashid = args.hashkey
  if hashid == None or hashid == '':
    print 'Specify HASHID to query!'
    exit(1)

  aa = QueryMovingPath()
  aa.query(hashid)

#
# main routine starts here
#
if __name__ == '__main__':
  main(sys.argv)

