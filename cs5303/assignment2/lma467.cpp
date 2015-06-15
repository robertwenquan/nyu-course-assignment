//

// Lola Ajayi

// CS5303 homework #2

/*

I understand that using, receiving or giving unauthorized assistance in

writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.

By submitting this work I am certifying that I did not cheat!

*/

#include<iostream>
using namespace std;
int main()
{
	float basic_charge, water_cost, total_bill, water_usage;
	int previous_reading, current_reading;

	cout << "Please enter your previous meter reading in cubic feet: \n";
	cin >> previous_reading;
	cout << "Your previous meter reading was " << previous_reading << " cubic feet." << "\n";
	cout << "Please enter your current meter reading in cubic feet: \n";
	cin >> current_reading;
	cout << "Your current meter reading is " << current_reading << " cubic feet." << "\n";
	water_usage = current_reading - previous_reading;
	water_usage = water_usage * 7.5;
	cout << "Your current water usage in gallons is " << water_usage << "." << "\n";
	water_usage = water_usage / 1000;
	basic_charge = 12.93;
	total_bill = basic_charge + (water_usage * 2.75);

	cout.setf(ios::fixed);
	cout.setf(ios::showpoint);
	cout.precision(2);

	cout << "Your total water bill for this quarter is " << "$" << total_bill << "." << "\n";
	return 0;

}