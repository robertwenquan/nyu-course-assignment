#!/bin/bash

gcc -c -o mod1.o mod1.c
gcc -c -o mod2.o mod2.c
gcc -o aa mod1.o mod2.o
