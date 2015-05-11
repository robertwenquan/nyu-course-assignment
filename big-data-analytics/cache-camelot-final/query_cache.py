#!/usr/bin/python

import sys
import pymongo
import argparse

# Open the MongoDB connection
def conn_open():
  global connMongo
  connMongo = pymongo.Connection('mongodb://localhost:27017')

  db = connMongo.camelot
  collection = db.smartcache

  return collection

# Close the MongoDB connection
def conn_close():
  connMongo.close()

def main(argv):

  parser = argparse.ArgumentParser()
  parser.add_argument('-k', '--hashkey', help='hashkey of the canvass map for query', type=str)
  args = parser.parse_args()

  hashid = args.hashkey
  if hashid == None or hashid == '':
    print 'Specify HASHID to query!'
    exit(1)

  connMongo = None
  collection = conn_open()

  for doc in collection.find({hashid:{"$exists": "true"}}, {"_id":0}):
    print doc[hashid]['1']
    print doc[hashid]['2']
    print doc[hashid]['3']

  conn_close()

#
# main routine starts here
#
if __name__ == '__main__':
  main(sys.argv)

