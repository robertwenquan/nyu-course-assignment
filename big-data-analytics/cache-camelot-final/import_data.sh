#!/bin/bash
#
# import_data.sh
#
# import smartcache data produced by the Map Reduce job
# the file is in JSON format
#
# EXAMPLE:
#  $ ./import_data.sh <JSON file1> <JSON file2> <JSON file3> ...
#
# OUTPUT:
#  In MongoDB, 
#  documents will be inserted into camilot.smartcache
#

DATABASE="camelot"
COLLECTION="smartcache"

if [ $# -lt 1 ]
then
  echo "Need files to be imported!"
  exit 2
fi

echo "db.dropDatabase()" | mongo $DATABASE

while [ $# -gt 1 ]
do
  INFILE=$1

  if [ ! -f "$INFILE" ]
  then
    echo "$INFILE does not exist!"
    shift
    continue
  fi

  shift

  mongoimport -d $DATABASE -c $COLLECTION --type json --file $INFILE
done

