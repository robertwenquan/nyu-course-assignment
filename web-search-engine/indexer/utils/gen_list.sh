#!/bin/bash

DIR="$1"
if [ ! -n "$DIR" ]
then
  DIR="test_data/output"
fi

ls -1 $DIR/*.[gm]it

