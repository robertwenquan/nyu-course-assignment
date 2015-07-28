#include <stdio.h>
#include <stdlib.h>

int main()
{
  float ff = 10;
  int aa = 0;

  printf("%f\n", ff);
  aa = 43;
  ff = (aa - 20)/10;
  printf("%f\n", ff);
  ff = 23/10;
  printf("%f\n", ff);
  return 0;
}

