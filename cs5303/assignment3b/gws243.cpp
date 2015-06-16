
//

// (Go Woon Seo)

// CS5303 homework #3-b

//

/*
 
 I understand that using, receiving or giving unauthorized assistance in
 
 writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.
 
 By submitting this work I am certifying that I did not cheat!
 
 */

#include <iostream>
using namespace std;

int main()
{
    cout.setf(ios::fixed);
    cout.setf(ios::showpoint);
    cout.precision(2);
    
    int month;
    double balance, payment, interest, shortage, rate, sum_interest;
    month = 0;
    balance = 0;
    payment = 100;
    interest = 0;
    rate = 0.001;
    shortage = 5000;
    sum_interest = 0;
    
    cout << "MONTH\t" << "BALANCE\t\t" << "PAYMENT\t\t" << "INTEREST\t" << "SHORTAGE" << endl;
    while ( shortage > 100)
    {
        month += 1;
        shortage = shortage - payment - interest;
        cout << month << "\t\t" << balance << "\t\t" << payment  << "\t\t" << interest  << "\t\t" << shortage << endl;
        balance = balance + payment + interest;
        interest = balance * rate;
        sum_interest = sum_interest + interest;
        
    }
    month += 1;
    balance = balance;
    interest = interest;
    payment = shortage - interest;
    shortage = shortage - payment - interest;
    sum_interest = sum_interest;
    
    cout << month << "\t\t" << balance << "\t\t" << payment  << "\t\t" << interest  << "\t\t" << shortage << endl;
    
    cout << "\nTotal number of months needed: " << month << endl;
    cout << "Total amount of interest earned: " << sum_interest << endl;
    
    return 0;
    
}
