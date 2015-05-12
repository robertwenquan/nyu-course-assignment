#!/bin/bash
#
# import_data.sh
#
# import smartcache data produced by the Map Reduce job
# the file is in JSON format
#
# EXAMPLE:
#  $ ./import_data.sh <JSON file>
#
# OUTPUT:
#  In MongoDB, 
#  documents will be inserted into camilot.smartcache
#

INFILE=$1

if [ ! -f "$INFILE" ]
then
  echo "$INFILE does not exist!"
  exit 2
fi

DATABASE="camilot"
COLLECTION="smartcache"

echo "db.dropDatabase()" | mongo $DATABASE
mongoimport -d $DATABASE -c $COLLECTION --type json --file $INFILE

