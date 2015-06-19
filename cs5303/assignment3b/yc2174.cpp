//

// Yajing Cai (yc2174)

// CS5303 homework #3b

/*
 I understand that using, receiving or giving unauthorized assistance in writing this assignment is
 inviolation of academic regulations and is subject to academic discipline, including a grade of 0 for this
 assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and
 dismissal from NYU.
 By submitting this work I am certifying that I did not cheat!
 */

#include <iostream>
using namespace std;

int main()
{
    float balance=0, payment=100, interest=0.0, shortage=5000,total_interest=0.0;
    int month=1;
    cout<<"month"<<"   "
        <<"Balance"<<"   "
        <<"Payment"<<"   "
        <<"interest"<<"   "
        <<"Shortage\n";
    cout.setf(ios::fixed);
    cout.setf(ios::showpoint);
    cout.precision(2);
    
    while (shortage > 0)
    {
        if (shortage < payment)
           {
             payment=shortage;
             shortage=0;
             interest=balance*0.001;
           }
        else
           {
              interest=balance*0.001;
              shortage=shortage-payment-interest;
           }
        
        cout<<month<<"       "
            <<balance<<"      "
            <<payment<<"    "
            <<interest<<"       "
            <<shortage<<"\n";
        month++;
        total_interest=total_interest+interest;
        balance=payment+balance+interest;
    }
    cout<<"\nTotal number of months needed: "<<month-1<<"\n"
        <<"\nTotal amount of interest earned: "<<total_interest;
    return 0;
}
