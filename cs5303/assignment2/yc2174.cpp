//
// Yajing Cai (yc2174)
// CS5303 homework #2
/*
 
 I understand that using, receiving or giving unauthorized assistance in
 writing this assignment is in violation of academic regulations and is
 subject to academic discipline, including a grade of 0 for this assignment
 with no chance of a making up the assignment, forfeiture of credit for the
 course, probation and dismissal from NYU.
 
 By submitting this work I am certifying that I did not cheat!
 
 */



#include<iostream>
using namespace std;

int main()
{
    cout.setf(ios::fixed);
    cout.setf(ios::showpoint);
    cout.precision(2);
    
    // declare variables
    float previousReadings=0.0;
    float currentReadings=0.0;
    float waterUsed=0.0;
    float totalCharge=0.0;
    
    //Enter input items
    cout<<" Enter the previous readings:";
    cin>>previousReadings;
    cout<<" Enter the current readings:";
    cin>>currentReadings;
    
    //calculates the water used and totalcharge
    waterUsed=currentReadings-previousReadings;
    totalCharge=waterUsed*7.5/1000*2.75+12.93;
    
    //output the totalcharge
    cout<<"totalCharge: $" <<totalCharge << endl;
    return 0;
}