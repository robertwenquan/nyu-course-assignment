//
// Go Woon Seo
// CS5303 homework #2
/*
I understand that using, receiving or giving unauthorized assistance in
writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment
with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.
*/

#include <iostream>
using namespace std;

int main()
{
	double water_cost, q_basic_charge, trans_unit, quater_bill;
	int current_meter, previous_meter;
	q_basic_charge = 12.93;
	water_cost = 2.75; // per 1000 gallon
	trans_unit = 7.5;

	cout << "What is an initial reading in cubic feet? ";
	cin >> previous_meter;
	cout << "what is a current reading in cubic feet? ";
	cin >> current_meter;

	quater_bill = (current_meter - previous_meter) * trans_unit / 1000 * water_cost +q_basic_charge;
	cout << "The water bill for the nextt quater is $";
	cout << quater_bill << endl;

	cout.precision(2);

	return 0;
}

