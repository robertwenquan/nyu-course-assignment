#include <iostream>
#include <cstdio>

/* parametric polymorphism */
template <class Type>
Type max(Type first, Type second) {
  return first > second ? first : second;
}

/* overloading + parametric polymorphism */
template <typename T>
T max(T a,T b,T c) {
  printf("sdff\n");
  if(b.val>a.val) a=b;
  if(c.val>a.val) a=c;

  return a;
}

int max(int a, int b) {
  if (a > b)
    return a;
  else
    return b;
}

int max(int a, int b, int c) {
  if (a > b && a > c)
    return a;
  else if (b > a && b > c)
    return b;
  else
    return c;
}

char max(char a, char b) {
  if (a > b)
    return a;
  else
    return b;
}

int main()
{
  int a, b, c;
  char d, e, f;

  a = 10;
  b = 33;

  d = 'x';
  e = 'b';

  c = max(a, b);
  f = max(d, e);

  printf("max(%d,%d) = %d\n", a, b, c);
  printf("max(%d,%d,%d) = %d\n", 3, 6, 1, max(3, 6, 1));
  printf("max(%c,%c) = %c\n", d, e, f);
}

