#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int main()
{
    unsigned char a1, b1;
    a1 = 185;
    b1 = 122;

    printf("a)))))))\n");
    printf("a1 - b1 = %d\n", a1 - b1);

    signed char a2, b2;
    a2 = 185;
    b2 = 122;

    printf("b)))))))\n");
    printf("a2 - b2 = %d\n", a2 + b2);

    signed char aa, bb, cc;
    aa = 151;
    bb = 214;
    cc = aa + bb;

    printf("c)))))))\n");
    printf("aa = %d\n", aa);
    printf("bb = %d\n", bb);
    printf("aa + bb = %d\n", cc);

    signed char a4, b4, c4;
    a4 = 151;
    b4 = 214;
    c4 = a4 - b4;

    printf("d)))))))\n");
    printf("a4 = %d\n", a4);
    printf("b4 = %d\n", b4);
    printf("a4 - b4 = %d\n", c4);

    int aaa[200] = {3,3,3,3};
    printf("aaa[18] = %d\n", aaa[113]);

    return 0;
}

