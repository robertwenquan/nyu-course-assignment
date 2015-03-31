#!/bin/bash

for n in 100 1000 10000 100000 1000000
do
  head -n $n flickr1m.log > flickr-${n}.log
done

