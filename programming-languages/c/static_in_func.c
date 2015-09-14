#include <stdio.h>

static int counter()
{
  static int x = 0;
  return x + 1;
}

static int counter2()
{
  static int x = 0;
  return ++x;
}

int main()
{
  printf("hello\n");

  int i = 0;
  for (i=0;i<10;i++)
  {
    printf("counter = %d\n", counter());
  }

  for (i=0;i<10;i++)
  {
    printf("counter2 = %d\n", counter2());
  }

  return 0;
}
