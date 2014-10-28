#!/usr/bin/python3

a=33
x=1
y=3
z=5

def sub1():
  a=7
  y=9
  z=11
  bb=33

  print("a(in sub1)=", a)

def sub2():
  global x
  a=13
  x=15
  w=17

  print("a(in sub2)=", a)

  def sub3():
    nonlocal a

    print("a(in sub3)=", a)

    a=19
    b=21
    z=23

    print("a(in sub3 end)=", a)

  sub3()

  print("a(in sub2 end)=", a)

print("a(outer)=", a)
sub1()
sub2()
print("a(outer)=", a)
