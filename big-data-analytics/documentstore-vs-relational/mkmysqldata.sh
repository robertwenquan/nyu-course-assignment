#!/bin/bash

for n in 100 1000 10000 100000 1000000
do
  infile="data/flickr-${n}.log"
  outfile="data/flickr-${n}.tab"

  echo "Making the data file for $infile ..."
  time ./json2tab.py $infile > $outfile
done

