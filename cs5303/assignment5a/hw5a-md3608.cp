//

// Mikhail Dvilyanski

// CS5303 homework #5a

/*

 I understand that using, receiving or giving unauthorized assistance in

 writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.

By submitting this work I am certifying that I did not cheat! 

*/

#include <iostream>
using namespace std;

//Function declaration for the function "mpg"
//that will calculate fuel efficiency
double mpg (double miles_par, double gallons_par);

//Function declaration for the function "tripcost"
//that will calculate the cost of the gasoline spent on the trip
double tripcost (double gallons_par, double price_par);

//Function declaration for the function "cost_per_student"
//that will calculate each student's share of the cost of the gasoline
double cost_per_student(double cost_par, int num_students_par);


int main ()
{
	//Variable declarations
	int num_students;	
	double miles, gallons, price, efficiency, total_cost, individual_cost;	
	char response;		//User's response on whether to repeat the calculation

	//Set decimal point output to 2 places
	cout.setf(ios::fixed);
	cout.setf(ios::showpoint);
	cout.precision(2);

	//Loop to perform repeated calculations at the user's request

	do
	{
	
		//Input values 
		cout << "Hello. Please enter the number of students: ";
		cin >> num_students;
		cout << "Please enter the number of miles traveled: ";
		cin >> miles;
		cout << "Please enter the number of gallons purchased at the end of the trip: ";
		cin >> gallons;
		cout << "Please enter the price per gallon of gasoline: ";
		cin >> price;

		//Function calls to compute results
		efficiency = mpg(miles, gallons);
		total_cost = tripcost(gallons, price);
		individual_cost = cost_per_student(total_cost, num_students);

		//Output results
		cout << "\nHere is some information about your trip: \n\n";
		cout << "Fuel efficiency: " << efficiency << " miles per gallon" << endl;
		cout << "Total cost of gasoline for the trip: $" << total_cost << endl;
		cout << "For " << num_students << " students, the cost of gasoline per student is: $" << individual_cost << endl << endl;

		cout << "Would you like to perform another computation? (Y/N): ";	
		cin >> response;
	}
	while (response == 'Y' || response == 'y');

	cout << "\n\nGood bye!\n\n";

	return 0;
}

//Function definitions

double mpg (double miles_par, double gallons_par)
{
	return (miles_par/gallons_par);
}

double tripcost (double gallons_par, double price_par)
{
	return (gallons_par * price_par);
}

double cost_per_student(double cost_par, int num_students_par)
{
	return (cost_par/num_students_par);
}



	

