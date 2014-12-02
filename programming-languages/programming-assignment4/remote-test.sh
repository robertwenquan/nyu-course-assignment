#!/bin/bash

export GOPATH="$PWD/qw476"
export PATH="$PATH:$GOPATH/bin"
unzip -o qw476.zip
cd qw476/src/unify
go install
cd -

if [ -x ./verify-case.sh ]
then
  ./verify-case.sh
fi

