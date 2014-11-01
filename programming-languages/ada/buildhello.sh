#!/bin/bash

#gcc -c hello.adb
#gnatbind hello
#gnatlink hello

gnatmake hello.adb -o hello
gnatmake stdio -o stdio
