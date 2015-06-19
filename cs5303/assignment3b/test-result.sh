#!/bin/bash

get_list_netid()
{
  ls -1 *.cpp | sed 's/\..*//g'
}

# print banner
for netid in $(get_list_netid)
do
  echo "Checking $netid"
  ./$netid > results/${netid}.log
  if [[ "$OSTYPE" == "darwin"* ]]
  then
    sed -e '/^ *$/d' -e 's/^ *//' -e 's/[ 	][ 	]*/	/g' -e 's/[ 	]*$//' results/${netid}.log | tr 'a-z' 'A-Z' > results/file1
    sed -e '/^ *$/d' -e 's/^ *//' -e 's/[ 	][ 	]*/	/g' -e 's/[ 	]*$//' results/standard.txt | tr 'a-z' 'A-Z' > results/file2
  elif [[ "$OSTYPE" == "linux-gnu" ]]
  then
    sed -e '/^ *$/d' -e 's/^ *//' -e 's/[ \t][ \t]*/\t/g' -e 's/[ \t]*$//' results/${netid}.log | tr 'a-z' 'A-Z' > results/file1
    sed -e '/^ *$/d' -e 's/^ *//' -e 's/[ \t][ \t]*/\t/g' -e 's/[ \t]*$//' results/standard.txt | tr 'a-z' 'A-Z' > results/file2
  else
    echo "Not supported"
    exit 0
  fi
  diff -u results/file1 results/file2
  rm -f results/file* &>/dev/null
  echo "======================="
done

