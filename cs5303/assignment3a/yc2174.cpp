//

// Yajing Cai (yc2174)

// CS5303 homework #3a

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
    int num_convert;
    
    cout << "Please input a whole number of inches less than 5,280: " ;
    cin >> num_convert;
    
    if (num_convert < 5280)
        cout<<"There are "
        << num_convert/36<<" yards, "
        << (num_convert%36)/12 <<" feet and "
        << (num_convert%36)%12 <<" inches in "
        << num_convert<<" inches.";
    else
        cout<< "Sorry, you were asked to enter a number less than 5,280.";
    
    return 0;
}