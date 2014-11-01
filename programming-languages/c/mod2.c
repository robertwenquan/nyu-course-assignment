#include <stdio.h>
#include <stdlib.h>

extern int get_a1();
extern int get_a2();
extern int static_get_a1();
extern int static_get_a2();

extern int a1;
extern int a2;

int main()
{
  printf("a1 = %d\n", get_a1());
  printf("a2 = %d\n", get_a2());
  printf("a1 = %d\n", a1);
  printf("a2 = %d\n", a2);
  printf("a1 = %d\n", static_get_a1());
  printf("a2 = %d\n", static_get_a2());
}

