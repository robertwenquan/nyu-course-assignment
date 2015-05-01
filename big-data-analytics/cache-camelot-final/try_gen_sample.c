#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
  int x = 0;
  int y = 0;

  int n = 0;

  for (x=0;x<14;x++) {
    for (y=0;y<8;y++) {
      n = x * 8 + y;
      printf("%d\n", n);
    }
  }
  return 0;
}
