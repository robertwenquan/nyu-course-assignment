#!/bin/bash

get_list_netid()
{
  ls -1 *.cpp | sed 's/\..*//g'
}

# print banner
for netid in $(get_list_netid)
do
  echo "Checking $netid"
  ./$netid | sed -e '/^ *$/d' -e 's/^ *//' -e 's/[ \t][ \t]*/\t/g' -e 's/[ \t]*$//' | tr 'a-z' 'A-Z' > results/file1
  cat results/standard.txt | sed -e '/^ *$/d' -e 's/^ *//' -e 's/[ \t][ \t]*/\t/g' -e 's/[ \t]*$//' | tr 'a-z' 'A-Z' > results/file2
  diff -u results/file1 results/file2
  echo "======================="
done

