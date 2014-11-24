#!/bin/bash

BIN="./assignment3.py"
BIN="./qw476"

ulimit -t 3

red='\e[0;31m'
green='\e[0;32m'
NC='\e[0m' # No Color

function time_diff()
{
  START=$1
  END=$2

  START_SEC=$(echo $START | cut -d- -f1)
  START_USEC=$(echo $START | cut -d- -f2)
  START_USEC=${START_USEC##*0}

  END_SEC=$(echo $END | cut -d- -f1)
  END_USEC=$(echo $END | cut -d- -f2)
  END_USEC=${END_USEC##*0}

  SEC_DIFF=$((END_SEC - START_SEC))
  USEC_DIFF=$((END_USEC - START_USEC))

  if [ $USEC_DIFF -lt 0 ]
  then
    USEC_DIFF=$((DIFF+1000000000))
    SEC_DIFF=$((SEC_DIFF-1))
  fi

  MS_DIFF=$(echo "scale=4;$SEC_DIFF*1000 + $USEC_DIFF/1000000.0" | bc)
  printf "%8.2f" $MS_DIFF
}


#
# main routine starts
#


if [ ! -x "$BIN" ]
then
  echo -e "${red}Executable $BIN is not found. Please double check if it's compiled correctly.${NC}"
  exit 1
fi

if [ ! -d testcases ]
then
  echo -e "${red}No testcases found. Have you created the test cases yet?${NC}"
  exit 1
fi

cnt=0
succ=0
fail=0

i=1
n=$(ls -1 testcases/case-*.input 2>/dev/null| wc -l)

if [ $n -eq 0 ]
then
  echo -e "${red}No testcases found in testcases directory. Have you created the test cases yet?${NC}"
  exit 1
fi

for case in $(ls -1 testcases/case-*.input 2>/dev/null)
do
  basename="${case%.*}"

  echo -ne "Test case [$i/$n]\t"
  cnt=$((cnt+1))

  output="${basename}.output"
  if [ -e "${output}" ]
  then
    EXEC_START=$(date +%s-%N)
    $BIN 2>&1 < $case | diff -u ${output} -
    if [ $? -eq 0 ]
    then
      EXEC_END=$(date +%s-%N)
      TIME_STR=$(time_diff "$EXEC_START" "$EXEC_END")
      printf "%-60s" $basename
      echo -e "\t${green}Pass${NC} in $TIME_STR ms"
      succ=$((succ+1))
    else
      echo -e "${red}Fail${NC}"
      fail=$((fail+1))
    fi
  else
    echo "<<< WARNING: No sample output file for $case !!!"
  fi

  i=$((i+1))
done

rate=$(echo "scale=4;$succ/$cnt*100" | bc)
echo
printf "Success [%d/%d], in %.2f%%\n" $succ $cnt $rate
