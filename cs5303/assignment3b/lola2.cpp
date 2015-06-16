//
//
//// Lola Ajayi
//
//// CS5303 homework #3b
//
////
//
///*
//
//I understand that using, receiving or giving unauthorized assistance in
//
//writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.
//
//By submitting this work I am certifying that I did not cheat!
//
//*/
//
#include <iostream>
using namespace std;
int
main ()
{
  int months = 1;
  float shortage = 5000, interest = 0, balance = 0, payment =
    0, total_interest = 0;

  cout.setf (ios::fixed);
  cout.setf (ios::showpoint);
  cout.precision (2);

  cout << "Month " << "Balance  " << "Payment  " << "Interest  " <<
    "Shortage\n";

  while (shortage >= 100)
    {
      interest = .001 * balance;
      payment = 100;
      shortage = 5000 - balance - payment - interest;
      cout << months << "     " << balance << "    " << payment << "      " <<
	interest << "   " << shortage << endl;
      balance = balance + payment + interest;
      months++;
      total_interest = total_interest + interest;

    }

  if (shortage > 0)
  {
    interest = .001 * balance;
    payment = shortage;
    shortage = 0;
    cout << months << "     " << balance << "    " << payment << "      " <<
	interest << "   " << shortage << endl;
    balance = balance + payment;
    months++;
    total_interest = total_interest;
  }

  cout << "Total number of months needed: " << months << endl;
  cout << "Total amount of interest earned is $" << total_interest << endl;
  return 0;
}

