//
// Wonil Chung
// CS5303 homework #2
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
    
    float cost = 2.75/1000;             // Water costs $2.75 per 1000 gallons
    float basic_connection = 12.93;     // Basic connect charge of $12.93 per quarter
    float CubicToGallon = 7.5;
    float previous = 0;
    float current = 0;
    
    cout<<"Please Enter Your Previous Meter Reading in Cubic Feet : \n";
    cin>>previous;
    cout<<"Your Previous Meter Reaing is "<<previous<<" Cubic Feet \n \n";
    
    cout<<"Please Enter Your Current Meter Reading in Cubic Feet : \n";
    cin>>current;
    cout<<"Your Current Meter Reaing is "<<current<<" Cubic Feet \n \n";
    
    float used = current - previous;
    cout<<"The Amount of Water Used is "<<used<<" Gallons \n";
    
    float bill = used*CubicToGallon*cost + basic_connection;
    cout<<"The Amount of Pending Quarterly Water Bill is $" << bill;

    return 0;
}
