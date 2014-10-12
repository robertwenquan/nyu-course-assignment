#!/bin/bash

gcc -c hello.adb
gnatbind hello
gnatlink hello
