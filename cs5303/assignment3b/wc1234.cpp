//
// Wonil Chung
// CS5303 homework #3b
/*
 I understand that using, receiving or giving unauthorized assistance in writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.
 By submitting this work I am certifying that I did not cheat!
 */

#include <iostream>
using namespace std;

int main()
{
    cout.setf(ios::fixed);
    cout.setf(ios::showpoint);
    cout.precision(2);
    
    int month = 1;
    int need = 5000;
    
    float balance = 0, payment = 100, interest = 0, shortage = need - payment, total_interest_paid = 0;;
    
    cout<<"MONTH"<<"\tBALANCE"<<"\t\tPAYMENT"<<"\t\tINTEREST"<<"\tSHORTAGE\n";
    
    while(shortage > 0){
        cout<<month<<"\t\t"<<balance<<"\t\t"<<payment<<"\t\t"<<interest<<"\t\t"<<shortage<<"\n";
        month += 1;
        balance += payment + interest;
        payment = payment;
        interest = ((1 + interest/100)*(1 + 0.1/100) - 1) * 100;
        shortage -= (payment + interest);
        total_interest_paid += interest;
        }
    
    float temp = shortage + payment + interest;
    payment = shortage + 100;
    shortage = temp - (payment + interest);
    
    cout<<month<<"\t\t"<<balance<<"\t\t"<<payment<<"\t\t"<<interest<<"\t\t"<<shortage<<"\n\n";
    
    cout<<"Total number of months needed: "<<month<<"\n";
    cout<<"Total amount of interest earned: "<<total_interest_paid<<"\n";
    
    return 0;
}