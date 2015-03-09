#!/bin/bash

MAPPER="./mapper.py"
REDUCER="./reducer.py"

INPUT="input/relation.map"
OUTPUT_IDX=0
OUTPUT=$(printf "output/output.%05d" $OUTPUT_IDX)

$MAPPER < $INPUT | $REDUCER > $OUTPUT
echo "Step 1 finishes"

NN=$(grep -E 'WAIT|TODO' $OUTPUT | wc -l)
echo $NN
while [ $NN -gt 0 ]
do
  INPUT=$(printf "output/output.%05d" ${OUTPUT_IDX})
  OUTPUT=$(printf "output/output.%05d" $((OUTPUT_IDX+1)))

  $MAPPER < $INPUT | $REDUCER > $OUTPUT
  NN=$(grep -E 'WAIT|TODO' $OUTPUT | wc -l)
  echo $NN

  OUTPUT_IDX=$((OUTPUT_IDX+1))
done

