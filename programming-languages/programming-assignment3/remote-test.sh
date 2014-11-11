#!/bin/bash

unzip -o qw476.zip
gnatmake *.adb -o assignment2

if [ -x ./verify-case.sh ]
then
  ./verify-case.sh
fi

