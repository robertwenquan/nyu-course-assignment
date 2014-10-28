#!/usr/bin/python3

g = 3
b = 56

def sub1():
  a = 5
  b = 7

  print("g in sub1() is" , g)

  def sub2():

    global g
    c = 9
    #b = 33
    print("g in sub2() is" , g)

    def sub3():
      nonlocal c
      #nonlocal b
      g = 11
      print("c in sub3() is" , c)
      print("g in sub3() is" , g)
      print("b in sub3() is" , b)

    sub3()

    print("g in sub2() is" , g)

  sub2()

sub1()
