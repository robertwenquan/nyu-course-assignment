//
//  main.cpp
//  prhw2
//
//  Created by Chase Jian on 6/2/15.
//  Copyright (c) 2015 Chase Jian. All rights reserved.
//

#include <iostream>
using namespace std;

int main(int argc, const char * argv[]) {
    //
    
    // Hailiang Jian
    // hj843
    // N10710571
    
    // CS5303 homework #2
    
    /*
     
     I understand that using, receiving or giving unauthorized assistance in
     
     writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.
     
     By submitting this work I am certifying that I did not cheat!
     
     */
    
    float previous, current, bill_amount;
    cout<<"Please input the previous meter reading in cubic feet:"<<endl;
    cin>>previous;
    cout<<"Please input the current meter reading in cubic feet:"<<endl;
    cin>>current;
    
    bill_amount=(current-previous)*7.5/1000*2.75+12.93;
    
    cout<<"The amount of the final bill is $"<<bill_amount<<"."<<endl;
    
    return 0;
}
