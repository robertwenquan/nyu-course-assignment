#!/bin/bash

generate_input()
{
    local n=$#
    local i=0

    for ((i=1;i<=n;i++))
    do
        echo ${!i}
    done
}

generate_output()
{
    echo $@ | awk 'BEGIN{
    len = 0
    sum = 0
    avg = 0.0
    min = 0
    max = 0
}

function print_stats()
{
    printf("%s%32d\n",   "Num: ", len)
    printf("%s%35.2f\n", "Sum: ", sum)
    printf("%s%35.2f\n", "Avg: ", avg)
    printf("%s%35.2f\n", "Min: ", min)
    printf("%s%35.2f\n", "Max: ", max)
}

{
    len = $1

    # TODOOOOOOOOO
    # handle error

    if (len !~ /[0-9]+/)
    {
        print "ERR"
        exit
    }
    else if (len == 0)
    {
        print_stats()
        next
    }

    if (len + 1 != NF)
    {
        print "ERR"
        exit
    }

    min = $2
    max = $2

    for (i=2;i<=NF;i++)
    {
        sum+=$i

        if ($i < min)
            min = $i

        if ($i > max)
            max = $i
    }

    avg = sum*1.0/len

    print_stats()
}'

}

verify_output()
{
    :
}

for file in $(ls -1 input*)
do
    while read LINE
    do
        IFS=","
        generate_output $LINE > /tmp/output1.asc
        generate_input $LINE | ./assignment1 > /tmp/output2.asc
        diff -u /tmp/output1.asc /tmp/output2.asc
    done < $file
done

