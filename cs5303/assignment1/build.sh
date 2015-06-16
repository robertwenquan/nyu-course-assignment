#!/bin/bash

for file in $(ls -1 *.cpp)
do
  echo "Building $file"
  binname=${file%%.*}
  g++ -o $binname $file
done
