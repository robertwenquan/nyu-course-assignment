#!/bin/bash

ghc qw476.hs

if [ -x ./verify-case.sh ]
then
  ./verify-case.sh
fi

