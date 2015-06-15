//
//  Jose Tomas Vicuna
//  CS5303 homework #2
//

/*
I understand that using, receiving or giving unauthorized assistance in writing this assignment is in violation of academic regulations and 
is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of 
credit for the course, probation and dismissal from NYU. By submitting this work I am certifying that I did not cheat!
*/

#include <iostream>
using namespace std;

int main() {
	char letter;

	cout.setf(ios::fixed);
	cout.setf(ios::showpoint);
	cout.precision(2);

	int currentReading;
	int previousReading;
	int actualReading;
	int currentGallons;
	double totalDue;

	const double CUBIC_FEET_IN_GALLONS = 7.5;
	const double BASIC_CONNECT_CHARGE = 12.93;
	const double WATER_COST = 2.75 / 1000;

	cout << "Welcome to your water bill calculator.\n\nPlease type the previous meter reading:";
	cin >> previousReading;
	cout << "Your previous meter reading is " << previousReading << ", thank you.\n\nNow please type your current meter reading:";
	cin >> currentReading;
	cout << "Your current meter reading is " << currentReading << ", thank you.\n" << endl;

	actualReading = currentReading - previousReading;

	cout << "Your actual reading is " << actualReading << " cubic feet." << endl << endl;

	currentGallons = actualReading*CUBIC_FEET_IN_GALLONS;

	cout << "This means you have used a total of " << currentGallons <<  " gallons of water." << endl << endl;

	totalDue = (WATER_COST*currentGallons) + BASIC_CONNECT_CHARGE;

	cout << "Your total amount due is: $" << totalDue << endl << endl << "Type any letter and press Enter to end.\n";
	cin >> letter;

	return 0;


}