#!/bin/bash

spit()
{
  while [ $# -gt 0 ]
  do
    printf "%s\t%d\n" $1 1
    shift
  done
}

while read LINE
do
  spit $LINE
done

