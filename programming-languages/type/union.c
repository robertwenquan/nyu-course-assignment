#include <stdio.h>
#include <string.h>

typedef union {
  struct {
    unsigned int bit1:1;
    unsigned int bit2:1;
    unsigned int bit3:1;
    unsigned int bit4:1;
    unsigned int bit5:1;
    unsigned int bit6:1;
    unsigned int bit7:1;
    unsigned int bit8:1;
    unsigned int bit9:1;
    unsigned int bit10:1;
    unsigned int bit11:1;
    unsigned int bit12:1;
    unsigned int bit13:1;
    unsigned int bit14:1;
    unsigned int bit15:1;
    unsigned int bit16:1;
  } bits;
  unsigned short bits_in_whole;
}  abc;

int main()
{
  abc a1;
  bzero(&a1, sizeof(abc));

  printf("size of unsigned short is: %d\n", sizeof(unsigned short));

  a1.bits.bit1 = 1;
  a1.bits.bit3 = 1;

  printf("%d\n", a1.bits_in_whole);
  return 0;
}

