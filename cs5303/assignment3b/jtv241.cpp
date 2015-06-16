//
//  Jose Tomas Vicuna
//  CS5303 homework #3b
//

/*
 I understand that using, receiving or giving unauthorized assistance in writing this assignment is in violation of academic regulations and
 is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of
 credit for the course, probation and dismissal from NYU. By submitting this work I am certifying that I did not cheat!
 */

#include <iostream>
#include <iomanip>
using namespace std;

int main(){
    
    cout.setf(ios::fixed);
    cout.setf(ios::showpoint);
    cout.precision(2);
    
    int MONEY_GOAL = 5000;
    
    int MONTH = 1;
    double BALANCE = 0;
    double PAYMENT = 100;
    double INTEREST = 0.001*BALANCE;
    double SHORTAGE = MONEY_GOAL-PAYMENT;
    
    double TOTAL_INTEREST_PAID = 0;

//Setting the table
    cout << setw(15) << left << "MONTH" << setw(15) << "BALANCE" << setw(15) << "PAYMENT"
        << setw(15) << "INTEREST" << "SHORTAGE\n";
    
//Setting the loop to fill out the table
    do{
        cout << setw(15) << left << MONTH << setw(15) << BALANCE << setw(15) << PAYMENT << setw(15) << INTEREST << SHORTAGE << endl;

        BALANCE += PAYMENT + INTEREST;
        INTEREST = 0.001*BALANCE;
        TOTAL_INTEREST_PAID += INTEREST;
        
        if((SHORTAGE)<=PAYMENT){
            PAYMENT = SHORTAGE - INTEREST;
        }
        
        SHORTAGE -= PAYMENT + INTEREST;
        MONTH++;
    }
    while (BALANCE <= MONEY_GOAL);
    
    cout << endl << "Total Interest Paid: " << TOTAL_INTEREST_PAID;
    
    return 0;

}

