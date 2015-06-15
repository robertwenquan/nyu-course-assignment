#!/bin/bash

BASE=12.93

for case in $(ls -1 testcases/*.input)
do
  xx=($(cat $case))
  START=${xx[0]}
  END=${xx[1]}

  echo $BASE $START $END
done

