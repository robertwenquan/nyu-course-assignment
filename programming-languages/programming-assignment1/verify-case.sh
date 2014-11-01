#!/bin/bash

BIN="./assignment1"

cnt=0
succ=0
fail=0
for case in $(ls -1 testcases/case* | grep -v output)
do
    cnt=$((cnt+1))

    output="${case}.output"
    if [ -e "${output}" ]
    then
        $BIN < $case | diff -u ${output} -
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
