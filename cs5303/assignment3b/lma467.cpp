#include <iostream>
using namespace std;
int
main ()
{
  int months = 1;
  float interest = 0, balance = 0, payment = 0, total_interest = 0;
  float shortage = 5000;
   cout.setf (ios::fixed);
  cout.setf (ios::showpoint);
  cout.precision (2);
   cout << "Month " << "Balance  " << "Payment  " << "Interest  " <<
    "Shortage\n";
   while (shortage > 100)

    {
      interest = .001 * balance;
      payment = 100;
      shortage = 5000 - balance - payment - interest;
      cout << months << "     " << balance << "    " << payment << "      "
	<< interest << "   " << shortage << endl;
      balance = balance + payment + interest;
      months++;
      total_interest = total_interest + interest;
     }
  balance = 5000 - shortage;
  interest = .001 * balance;
  payment = shortage - interest;
  shortage = 5000 - balance - payment - interest;
  cout << months << "     " << balance << "    " << payment << "      " <<
    interest << "   " << shortage << endl;
  total_interest = total_interest + interest;
   cout << "Total number of months needed: " << months << endl;
  cout << "Total amount of interest earned is $" << total_interest << endl;
  return 0;
}
