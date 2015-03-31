#!/bin/bash

for n in 100 1000 10000 100000 1000000
do
  infile="data/flickr-${n}.log"
  outfile="data/flickr-${n}.sql"

  echo "Making SQL data for $infile ..."
  time ./json2sql.py $infile > $outfile
done

