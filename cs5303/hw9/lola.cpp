//
// Lola M. Ajayi
// CS5303 homework #9
/*
I understand that using, receiving or giving unauthorized assistance in
writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.
By submitting this work I am certifying that I did not cheat!
*/

#include <iostream>
using namespace std;

int main()
{
	long int number;
	int digit;
	char choice;
	const int number_digits = 10;

	bool digits_seen[number_digits];
	for (int i = 0; i < number_digits; i++)
		digits_seen[i] = false;
do
	{
		cout << "Please enter a number: ";
		cin >> number;
	
		while (number > 0)
			{
				digit = number % 10;
				if (digits_seen[digit] == false)
					digits_seen[digit] = true;
				else
					break;
				number = number / 10;
			}

		if (number > 0)
			{
				cout << "It has repeated digit" << endl;
				cout << "Do you want to enter another number? (y/n)";
				cin >> choice;
			}

		else
			{
				cout << "No repeat" << endl;
				cout << "Do you want to enter another number? (y/n)";
				cin >> choice;
			}
		
	} while ((choice == 'Y') || (choice == 'y'));

return 0;

}
