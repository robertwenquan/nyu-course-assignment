#include <stdio.h>
#include <stdlib.h>

int a1 = 11;
static int a2 = 222;

int get_a1(){
  return a1;
}

static int static_get_a1(){
  return a1;
}

int get_a2(){
  return a2;
}

static int static_get_a2(){
  return a2;
}

