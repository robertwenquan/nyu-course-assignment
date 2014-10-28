#!/usr/bin/python3

g = 3
b = 56

def sub1():
    a = 5
    b = 7

def sub2():
    global g
    c = 9

    def sub3():
      nonlocal c
      g = 11

      sub3()

    sub2()

sub1()
