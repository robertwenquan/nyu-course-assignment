#!/bin/bash

for n in 100 1000 10000 100000 1000000
do
  infile="data/flickr-${n}.log"
  echo "Loading $infile"
  time mongoimport -d qw476 -c flickr_pics --type json --file $infile

  echo "Test query"
  time mongo qw476 < test/query.mongo >/dev/null

  echo "Test query"
  time mongo qw476 < test/query2.mongo >/dev/null

  echo "Test update"
  time mongo qw476 < test/update.mongo

  echo "Complex Query"
  time mongo qw476 < test/complex.mongo >/dev/null

  echo "Test delete"
  time mongo qw476 < test/delete.mongo

done

