//
// Go Woon Seo
// CS5303 homework #5a
/*
 I understand that using, receiving or giving unauthorized assistance in
 writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment
 with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.
 */

#include <iostream>
using namespace std;


double milepergallon(double miles, double gallons);
double tripcost(double gallons, double gasprice);
double amountforeach(int std, double tc);

int main() {
    
    cout.setf(ios::fixed);
    cout.setf(ios::showpoint);
    cout.precision(2);
    
    char repeat;
    int std;
    double miles, gallons, gasprice, tc;

    do {
        cout << "How many students went on the trip? ";
        cin >> std;
        cout << "\n";
        
        cout << "How many miles did they travel? ";
        cin >> miles;
        cout << "\n";
        
        cout << "How many gallons did they use? ";
        cin >> gallons;
        cout << "\n";
        
        cout << "What was the price per gallon? ";
        cin >> gasprice;
        cout << "\n";
        
        if ((std < 0) || (miles<0) || (gallons <0) || (gasprice <0)) {
            cout << "Error : Please restart this program and enter the non-negative values!\n";
            return 0;
        }
        
        tc = tripcost(gallons, gasprice);
        
        cout << "You travelled "<< miles << " miles on " << gallons << " gallons of gasoline which was $" << milepergallon(miles, gallons) << " miles per gallon\n\n";
        
        cout << "The cost of the trip was $"<< tc << ", so each student pays $" << amountforeach(std, tc) << "\n\n";
        
        cout << "Do you want to do this calculation again? (y/n) ";
        cin >> repeat;
        
        if ((repeat == 'n')||(repeat == 'N')) return 0;
        else if ((repeat != 'y')&&(repeat != 'Y')&&(repeat !='n')&&(repeat!='N')){
            cout << "Please enter either Y(y) or N(n) : " ;
            cin >> repeat;
            cout << "\n\n";
        }
        
    } while ((repeat == 'y')||(repeat == 'Y'));
    
    
    return 0;
    
}

double milepergallon(double miles2, double gallons2){
    
    return miles2/gallons2;
}

double tripcost(double gallons3, double gasprice2){
    
    return gallons3 * gasprice2;
}

double amountforeach(int std2, double cost){
    
    return cost / std2;
}

