//

// Mikhail Dvilyanski

// CS5303 homework #3a

/*

 I understand that using, receiving or giving unauthorized assistance in

 writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.

By submitting this work I am certifying that I did not cheat! 

*/

#include <iostream>
using namespace std;

int main ()
{
	int total_inches, inches, yards, feet, remainder;	//Declare variables
	
	cout << "Hello. Please input a whole number of inches less than 5,280: \n";
	cin >> total_inches;      //Input total number of inches

	if (total_inches < 5280)      //Verify that the number of inches inputted is less 5,280
	{
		yards = total_inches/36;	//Calculate yards
		remainder = total_inches%36;	//Remaining inches after yards calculation
		feet = remainder/12;		//Calculate feet
		inches = remainder%12;		//Remaining inches after yards and feet calculation
		
		//Output results
		cout << "There are " << yards << " yards, " << feet << " feet and " 
			<< inches << " inches in " << total_inches << " inches.\n\n";
	}
	else
		cout << "\nSorry, you were asked to enter a number less than 5,280\n";
	
	return 0;
}
		

		
	
