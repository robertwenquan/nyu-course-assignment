//

// Lola M. Ajayi

// CS5303 homework #5a

//

/*

I understand that using, receiving or giving unauthorized assistance in

writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.

By submitting this work I am certifying that I did not cheat!

*/

#include <iostream>
using namespace std;

double fuel_efficiency(double miles, double gallons);
double trip_cost(double gallons, double price);
double student_cost(double price, int students);

int main()
{
	cout.setf(ios::fixed);
	cout.setf(ios::showpoint);
	cout.precision(2);

	int students;
	double miles_traveled, gallons_purchased, price_gas, total_cost;
	char choice;
	do
	{
		cout << "How many students went on the trip? ";
		cin >> students;
		cout << "How many miles did they travel? ";
		cin >> miles_traveled;
		cout << "How many gallons did they use? ";
		cin >> gallons_purchased;
		cout << "What was the price per gallon? ";
		cin >> price_gas;


		cout << "You travelled " << miles_traveled << " miles on " << gallons_purchased
			<< " gallons of gasoline which was " << fuel_efficiency(miles_traveled, gallons_purchased)
			<< " miles per gallon\n";

			total_cost = trip_cost(gallons_purchased, price_gas);

		cout << "The cost of the trip was $" << total_cost
			<< ", so each student pays $" << student_cost(total_cost, students) << endl;

		cout << "Do you want to do this calculation again? (y/n)";
		cin >> choice;
	} while ((choice == 'Y') || (choice == 'y'));
	return 0;
}

double fuel_efficiency(double miles, double gallons)
{
	return (miles / gallons);
}

double trip_cost(double gallons, double price)
{
	return (gallons*price);
}

double student_cost(double price, int student)
{
	return (price / student);
}