//
//  main.cpp
//  prhw3
//
//  Created by Chase Jian on 6/10/15.
//  Copyright (c) 2015 Chase Jian. All rights reserved.
//

#include <iostream>
using namespace std;

int main(int argc, const char * argv[]) {
    // insert code here...
    int number;
    int yard, foot, inch;
    
    for(int i=0; i<2; i++)
    {
        cout<<"Input a whole number of inches less than 5,280:"<<endl;
        cin>>number;
    
        if(number >= 5280)
            cout<<"Sorry, you were asked to enter a number less than 5,280."<<endl;
        else
        {
            yard = number/36;
            foot = (number%36)/12;
            inch = ((number-yard*36)%12)/1;
        
            cout<<"There are "<<yard<<" yards, "<<foot<<" feet and "<<inch<<" inches in "<<number<<" inches."<<endl;
        }
        cout<<endl;
    }
    return 0;
}
