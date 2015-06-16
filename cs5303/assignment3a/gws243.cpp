
//

// (Go Woon Seo)

// CS5303 homework #3-a

//

/*

I understand that using, receiving or giving unauthorized assistance in

writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.

By submitting this work I am certifying that I did not cheat!

*/

#include <iostream>
using namespace std;

int main()
{
	int num1, yards, feet, inches;
	cout << "Please enter a whole number of inches less than 5,280 : \n";
	cin >> num1;

	if (num1 < 5280)
	{
		yards = num1 / 36;
		feet = (num1 - yards * 36) / 12;
		inches = num1 - yards * 36 - feet * 12;
		cout << "There are " << yards << " yards, " << feet << " feet and " << inches << " inches in " << num1 << " inches. \n";
	}

	else
	{
		cout << "Sorry, you were asked to enter a number less than 5,280 \n";
	}

	return 0;
}


