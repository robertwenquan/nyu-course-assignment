//
// Wonil Chung
// CS5303 homework #3a
/*
 I understand that using, receiving or giving unauthorized assistance in writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.
 By submitting this work I am certifying that I did not cheat!
 */

#include <iostream>
using namespace std;

int main()
{
    int inch;
    
    cout<<"Enter an integer of inches : \n";
    cin>>inch;
    cout<<"The integer you typed is "<<inch<<" inches \n";
    
    if(inch>=5280){
        cout<<"Sorry, you were asked to enter a number less than 5280 \n";
    }
    else if(inch<0){
        cout<<"Sorry, you were asked to enter a number larger than 0 \n";
    }
    else{
        int yard = 0;
        int foot = 0;
        int _inch = 0;
        
        yard = inch/36;
        foot = (inch - yard*36)/12;
        _inch = inch%12;
        cout<<"There are "<<yard<<" yards, "<<foot<<" feet and "<<_inch<<" inches in "<<inch<<" inches \n";
    }
    
    return 0;
}