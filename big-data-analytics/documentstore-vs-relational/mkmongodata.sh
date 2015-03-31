#!/bin/bash

for n in 100 1000 10000 100000 1000000
do
  infile="data/flickr-${n}.log"
  outfile="data/flickr-${n}.mongo"

  echo "Making Mongo data for $infile ..."
  time ./json2mongo.py $infile > $outfile
done

