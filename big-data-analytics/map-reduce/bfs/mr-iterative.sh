#!/bin/bash

MAPPER="mapper.py"
REDUCER="reducer.py"

INPUT="/user/robert/bfs/input/relation.map"
OUTPUT_IDX=0
OUTPUT=$(printf "/user/robert/bfs/output.%05d" $OUTPUT_IDX)
OUTPUT_LOCAL="output/part-$(printf %05d $OUTPUT_IDX)"

STREAM_LIB="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.6.0.jar"

hadoop jar $STREAM_LIB -input $INPUT -output $OUTPUT -mapper $MAPPER -reducer $REDUCER
hadoop fs -copyToLocal $OUTPUT/part-00000 $OUTPUT_LOCAL
echo "Step 1 finishes"

NN=$(grep -E 'WAIT|TODO' $OUTPUT_LOCAL | wc -l)
echo $NN
while [ $NN -gt 0 ]
do
  INPUT=$(printf "/user/robert/bfs/output.%05d" ${OUTPUT_IDX})
  OUTPUT=$(printf "/user/robert/bfs/output.%05d" $((OUTPUT_IDX+1)))

  hadoop jar $STREAM_LIB -input $INPUT -output $OUTPUT -mapper $MAPPER -reducer $REDUCER

  OUTPUT_LOCAL="output/part-$(printf %05d $((OUTPUT_IDX+1)))"
  hadoop fs -copyToLocal $OUTPUT/part-00000 $OUTPUT_LOCAL

  NN=$(grep -E 'WAIT|TODO' $OUTPUT_LOCAL | wc -l)
  echo $NN

  OUTPUT_IDX=$((OUTPUT_IDX+1))
done

