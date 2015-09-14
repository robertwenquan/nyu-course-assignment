// my first program in C++
#include <iostream>

int main()
{
  bool digits_seen[10] = { false, true, true, false, true, false, false, false, false, false };

  float ff = 10.0000;
  std::cout << ff << "\n";
  ff = 23/10;
  std::cout << ff << "\n";
  ff = float(23/10);
  std::cout << ff << "\n";
  // read a number, dissect each digit and print only the numbers that were pre-set to be true
}

