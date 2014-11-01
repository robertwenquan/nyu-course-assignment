#!/bin/bash

yorn() {
  echo -n "${1:-Press Y or N to continue: }"
 
#  shopt -s nocasematch
 stty -echo -icanon
 
  until [[ "$ans" == [yn] ]]
  do
    #read -s -n2 ans
    read -n1 ans
  done
 
  echo "$ans"
 
 stty echo icanon
#  shopt -u nocasematch
}
 
case $- in
  *i*) echo "This shell is interactive";;
    *) echo "This is a script";;
esac

yorn

#stty -echo -icanon

#read A
#echo $A

#stty echo icanon
