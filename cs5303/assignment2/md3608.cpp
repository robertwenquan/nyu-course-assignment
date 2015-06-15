//

// Mikhail Dvilyanski

// CS5303 homework #2

/*
I understand that using, receiving or giving unauthorized assistance in
writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.

By submitting this work I am certifying that I did not cheat! 
*/

#include <iostream>
using namespace std;

int main ()
{
	double previous_reading, current_reading, gallons_used, current_bill, connect_charge, k, unit_cost;
	
	k = 7.5; 		//Constant for number of gallons in a cubic foot
	connect_charge = 12.93; //Connection charge per quarter
	unit_cost = 2.75/1000; 	//Cost in dollars per 1 gallon of water

	cout << "\nHello. Please enter previous quarter's meter reading (in cubic feet): ";
	cin >> previous_reading; //Input value for previous meter reading
	cout << "\nPlease enter current meter reading (in cubic feet): ";
	cin >> current_reading;  //Input value for current meter reading
	gallons_used = k*(current_reading - previous_reading);  //Calculate gallons used this quarter
	current_bill = connect_charge + unit_cost*gallons_used; //Calculate current bill
	
	//Set out to 2 decimal places
	cout.setf(ios::fixed); 
	cout.setf(ios::showpoint);
	cout.precision(2);

	//Output result
	cout << "\n\n**********************************************\n\n";
	cout << gallons_used << " gallons of water were used this period\n\n";
	cout << "The pending bill is: $" << current_bill << endl;
	cout << "\nThank you.\n**********\n\n";
}
