//
//  main.cpp
//  hw3b
//
//  Created by Chase Jian on 6/12/15.
//  Copyright (c) 2015 Chase Jian. All rights reserved.
//

#include <iostream>
#include <iomanip>
using namespace std;

int main(int argc, const char * argv[]) {
    
    double balance[100], payment[100], shortage[100];
    int month=0;//number of month needed
    int flag=0;
    double TOTAL_INTEREST_PAID=0.00;
 cout<<setw(10)<<left<<"MONTH"<<setw(10)<<left<<"BALANCE"<<setw(10)<<left<<"PAYMENT"<<setw(10)<<left<<"INTEREST"<<setw(10)<<left<<"SHORTAGE"<<endl;
    
    for(int i = 1; i<100; i++)
    {
        if(i!=1)
        {
            balance[i] = 5000.00 - shortage[i-1];
            if(shortage[i-1]<100)
            {
                payment[i] = 5000.00-balance[i]-balance[i]*0.001;
                flag = 1;
            }
            else
                payment[i] = 100;
        }
        else
        {
            balance[i] = 0.00;
            payment[i] = 100;
        }
        shortage[i]= 5000.00-balance[i]-payment[i]-balance[i]*0.001;
        month++;
        TOTAL_INTEREST_PAID+= balance[i]*0.001;
        cout<<setw(10)<<left<<i<<setw(10)<<setprecision(2)<<setiosflags(ios::fixed)<<left<<balance[i]<<setw(10)<<setprecision(2)<<setiosflags(ios::fixed)<<left<<payment[i]<<setw(10)<<setprecision(2)<<left<<setprecision(2)<<balance[i]*0.001<<setw(10)<<setprecision(2)<<setiosflags(ios::fixed)<<left<<shortage[i]<<endl;
        if(flag==1)
            break;
    }
    cout<<endl<<endl;
    cout<<"Total number of months needed: "<<month<<endl;
    cout<<"Total amount of interest earned: "<<setprecision(2)<<setiosflags(ios::fixed)<<TOTAL_INTEREST_PAID<<endl;
    
    return 0;
}



