#!/bin/bash

BIN="./assignment2"

cnt=0
succ=0
fail=0
for case in $(ls -1 testcases/case-*.input)
do
  #filename="${case##*/}"
  basename="${case%.*}"

  cnt=$((cnt+1))

  output="${basename}.output"
  if [ -e "${output}" ]
  then
    $BIN 2>&1 < $case | diff -u ${output} -
    if [ $? -eq 0 ]
    then
      succ=$((succ+1))
    else
      fail=$((fail+1))
    fi
  else
    echo "<<< WARNING: No sample output file for $case !!!"
  fi
done

rate=$(echo "scale=4;$succ/$cnt*100" | bc)
echo
echo
printf "Success [%d/%d], in %.2f%%\n" $succ $cnt $rate
