#!/bin/bash

i=0

while read LINE
do
  ./draw_canvass.R $LINE ${i}.png
  i=$((i+1))
done < list

