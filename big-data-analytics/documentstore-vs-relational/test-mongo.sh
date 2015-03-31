#!/bin/bash

for n in 100 1000 10000 100000 1000000
do
  infile="data/flickr-${n}.mongo"
  echo "Loading $infile"
  #time mongoimport -d qw476 -c flickr_pics --type json --file $infile
  time mongo qw476 < $infile
  #echo "Test query"
  #time mysql -u qw476 -uqw476123 test < test/query.sql
  #echo "Test update"
  #time mysql -u qw476 -uqw476123 test < test/update.sql
  echo "Test delete"
  time mongo qw476 < test/delete.sql
done

