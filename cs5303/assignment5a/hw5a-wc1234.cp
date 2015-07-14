//
// Wonil Chung
// CS5303 homework #5a
/*
 I understand that using, receiving or giving unauthorized assistance in writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.
 By submitting this work I am certifying that I did not cheat!
 */

#include <iostream>
using namespace std;

double FuelEfficiency(double _mile, double _gallon);
double CostOfTrip(double _gallon, double _gas_price);
double StudentPayment(double _costofgasoline, int _student);

int main()
{
    cout.setf(ios::fixed);
    cout.setf(ios::showpoint);
    cout.precision(2);
    
    int student = 0;
    double mile = 0, gallon = 0, gas_price = 0, costofgasoline = 0;
    char calculation_again = 'n';
    cout<<"How many students went on the trip? ";
    cin>>student;
    
    cout<<"How many miles did they travel? ";
    cin>>mile;
    
    cout<<"How many gallons did they use? ";
    cin>>gallon;
    
    cout<<"What was the price per gallon? ";
    cin>>gas_price;
    cout<<endl;

    if((student > 2147483647) || (mile > 2147483647) || (gallon > 2147483647) || (gas_price > 2147483647) ||
       (student <= 0) || (mile <= 0) || (gallon <= 0) || (gas_price <= 0) || ((student*1000)%1000 != 0)){
        cout<<"Error!!! Type Valid Value!!!"<<endl;
    }
    else{
    cout<<"You travelled "<<mile<<" miles on "<<gallon<<" gallons of gasoline which was "
        <<FuelEfficiency(mile, gallon)<<" miles per gallon."<<endl;
    
    cout<<"The cost of the trip was $"<<CostOfTrip(gallon, gas_price)
        <<", so each student pays $";
    costofgasoline = CostOfTrip(gallon, gas_price);
    cout<<StudentPayment(costofgasoline, student)<<endl;
    cout<<endl;

    cout<<"Do you want to do this calculation again? (y/n) ";
    cin>>calculation_again;
    
    while(calculation_again == 'y')
    {
        cout<<"How many students went on the trip? ";
        cin>>student;
        
        cout<<"How many miles did they travel? ";
        cin>>mile;
        
        cout<<"How many gallons did they use? ";
        cin>>gallon;
        
        cout<<"What was the price per gallon? ";
        cin>>gas_price;
        cout<<endl;
        
        if((student > 2147483647) || (mile > 2147483647) || (gallon > 2147483647) || (gas_price > 2147483647) ||
           (student <= 0) || (mile <= 0) || (gallon <= 0) || (gas_price <= 0) || ((student*1000)%1000 != 0)){
               cout<<"Error!!! Type Valid Value!!!"<<endl;
           }
           else{
               cout<<"You travelled "<<mile<<" miles on "<<gallon<<" gallons of gasoline which was "
               <<FuelEfficiency(mile, gallon)<<" miles per gallon."<<endl;
               
               cout<<"The cost of the trip was $"<<CostOfTrip(gallon, gas_price)
               <<", so each student pays $";
               costofgasoline = CostOfTrip(gallon, gas_price);
               cout<<StudentPayment(costofgasoline, student)<<endl;
               cout<<endl;

               cout<<"Do you want to do this calculation again? (y/n) ";
               cin>>calculation_again;
           }
    }
    }
    return 0;
}

double FuelEfficiency(double _mile, double _gallon)
{
    double fuel_efficiency = _mile/_gallon;
    return fuel_efficiency;
}

double CostOfTrip(double _gallon, double _gas_price)
{
    double costoftrip = _gallon * _gas_price;
    return costoftrip;
}

double StudentPayment(double _costofgasoline, int _student)
{
    double student_payment = _costofgasoline/_student;
    return student_payment;
}
