#!/bin/bash
#
# count how many lines of source code lines per language
# are written for this project
#
# TODO: add breakdown by person who last updated it
#

for file in $(find . | grep -E "\.([ch]|py|md)$")
do
  wc -l $file
done | sort -t. -k3 | awk 'BEGIN{
  FS=".";
}
{
  count[$3] += int($1);
  total += int($1);
}
END{
  for (ii in count)
  {
    print ii, "file: ", count[ii];
  }
  print "totol: ", total
}'

