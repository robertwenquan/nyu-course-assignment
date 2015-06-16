//
//  Jose Tomas Vicuna
//  CS5303 homework #3a
//

/*
 I understand that using, receiving or giving unauthorized assistance in writing this assignment is in violation of academic regulations and
 is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of
 credit for the course, probation and dismissal from NYU. By submitting this work I am certifying that I did not cheat!
 */

#include<iostream>
using namespace std;

int main (){
    
    int userInches;
    int userFeet;
    int userYards;
    int firstValue;
    
    const int feet = 12;
    const int yards = 3*feet;
    
    cout << "Hello, please input a whole number of inches, less than 5,280.\n";
    cin >> userInches;
    firstValue = userInches;
    
    if(userInches < 5280){
    
        userYards = (userInches/yards);
        userFeet = ((userInches%yards)/feet);
        userInches = ((userInches%yards)%feet);
        
        cout << "There are " << userYards << " yards, " << userFeet << " feets and " << userInches << " inches in " << firstValue << " inches.";
    }
    
    else{
        cout << "I'm sorry, but the number you entered is greater than 5,280";
    }
    
    return 0;
}
