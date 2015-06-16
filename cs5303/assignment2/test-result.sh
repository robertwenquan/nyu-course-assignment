#!/bin/bash

get_list_netid()
{
  ls -1 *.cpp | sed 's/\..*//g'
}

# print banner
printf "%15s" " "
for netid in $(get_list_netid)
do
  printf "%15s" "$netid"
done
echo

for case in $(ls -1 testcases/*.input)
do
  casefile=${case##*/}
  casefile=${casefile%%.*}

  printf "%15s" "$casefile"
  for netid in $(get_list_netid)
  do
    result=$(./$netid < $case | grep -o '\$.*' | sed 's/\.$//') 
    printf "%15s" "$result"
  done

  echo

done

