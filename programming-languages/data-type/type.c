#include <stdio.h>

struct abc {
  int inta;
  float floata;
  long longa;
  char str[100];
};

int main()
{
  printf("sizeof(char) = %d\n", sizeof(char));
  printf("sizeof(short) = %d\n", sizeof(short));
  printf("sizeof(int) = %d\n", sizeof(int));
  printf("sizeof(long) = %d\n", sizeof(long));
  printf("sizeof(long long) = %d\n", sizeof(long long));
  printf("sizeof(float) = %d\n", sizeof(float));
  printf("sizeof(double) = %d\n", sizeof(double));
  printf("sizeof(long *) = %d\n", sizeof(long *));
  printf("sizeof(int *) = %d\n", sizeof(int *));
  printf("sizeof(struct {int,float,long,char[100]}) = %d\n", sizeof(struct abc));
}

