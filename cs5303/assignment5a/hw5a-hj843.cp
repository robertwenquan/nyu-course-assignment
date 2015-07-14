//
//  main.cpp
//  hw5a
//
//  Created by Chase Jian on 6/24/15.
//  Copyright (c) 2015 Chase Jian. All rights reserved.
//

#include <iostream>
#include <iomanip>
using namespace std;

double FuelEfficiency(double distance, double gallon);
double Cost(double gallon, double price);
double AmoutEach(double cost, int stu_number);

int main(int argc, const char * argv[]) {
    int num_student;
    double distance, gallon, price, cost, efficiency, amouteach;
    char yorn;
    
    do
    {
        cout<<"How many students went on the trip? ";
        cin >> num_student;
        cout<<"How many miles did they travel? ";
        cin>>distance;
        cout<<"How many gallons did they use? ";
        cin>>gallon;
        cout<<"What was the price per gallon? ";
        cin>>price;
    
        efficiency = FuelEfficiency(distance,gallon);
        cost = Cost(gallon, price);
        amouteach = AmoutEach(cost, num_student);
    
        cout<<"You travelled "<<setiosflags(ios::fixed)<<setprecision(2)<<distance<<" miles on "<<setiosflags(ios::fixed)<<setprecision(2)<<gallon<<" gallons of gasoline which was "<<setiosflags(ios::fixed)<<setprecision(2)<<efficiency<<" miles per gallon"<<endl;
        cout<<"The cost of the trip was $"<<setiosflags(ios::fixed)<<setprecision(2)<<cost<<", so each student pays $"<<setiosflags(ios::fixed)<<amouteach<<endl;
        cout<<endl<<"Do you want to do this calculation again?  (y/n) ";
        cin>>yorn;
    }while(yorn == 'y');
    return 0;
}


double FuelEfficiency(double distance, double gallon)
{
    return distance/gallon;
}

double Cost(double gallon, double price)
{
    return gallon*price;
}

double AmoutEach(double cost, int stu_number)
{
    return cost/stu_number;
}