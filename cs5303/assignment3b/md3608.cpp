//

// Mikhail Dvilyanski

// CS5303 homework #3b

/*

 I understand that using, receiving or giving unauthorized assistance in

 writing this assignment is in violation of academic regulations and is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of credit for the course, probation and dismissal from NYU.

By submitting this work I am certifying that I did not cheat! 

*/

#include <iostream>
using namespace std;

int main ()
{
	//Variable declarations
	int downpayment;
	int count = 1;	//Declare counter to calculate number of months					
	double monthly_payment, balance, shortage, interest, total_interest_paid;	

	downpayment = 5000;		//Initialize downpayment amount
	monthly_payment = 100;		//Initialize monthly payment amount
	balance = 0;			//Starting balance
	interest = 0;			//Initialize interest to 0
	total_interest_paid = 0;	//Initialize cumulative interest to 0
	shortage = downpayment - monthly_payment;      //Initialize shortage after first month's payment

	
	//Set decimal point output to 2 places for money
	cout.setf(ios::fixed);
	cout.setf(ios::showpoint);
	cout.precision(2);

	//Output the headings and first values after first month of payments
	cout << "MONTH     BALANCE     PAYMENT     INTEREST     SHORTAGE\n\n";
	cout << count << "\t  " << balance << "\t\t" << monthly_payment << 
			"\t    " << interest << "\t" << shortage << endl;

	//The while loop will continue the calculation as long as the monthly payment
	//remains $100. Once the monthly payment is less than $100, that means we are
	//entering the last month of payments
	while (monthly_payment >= 100)		
	{
		count++;		//Increase number of months by 1
		balance = balance + monthly_payment + interest; //Calculate balance after this month's payment
		interest = balance * 0.001;  //Calculate interest based on current balance
		shortage = downpayment - balance - monthly_payment- interest; //Remaining shortage to pay
		total_interest_paid = total_interest_paid + interest;	//Cumulative interest	
		
		//Output results for current monthly cycle
		cout << count << "\t  " << balance << "\t" << monthly_payment << 
			"\t    " << interest << "\t" << shortage << endl;
		
		//Once remaining shortage is less than the monthly payment ($100)
		//we need to recalculate the amount of the last monthly payment
		if (shortage < 100)
		{	
			count ++;		//Increase number of months
			balance = balance + monthly_payment + interest;	//This is the last balance before the final monthly payment
			interest = balance * 0.001;		//Interest based on current balance
			monthly_payment = downpayment - balance - interest; //Recalculate final monthly payment
			total_interest_paid = total_interest_paid + interest; //Cumulative interest
			shortage = downpayment - balance - monthly_payment- interest; //Last shortage, which should be 0
			
			//Output results for the final month
			cout << count << "\t  " << balance << "\t" << monthly_payment << 
			"\t    " << interest << "\t" << shortage << endl;
		}

	}
	
	//Output total number of months to pay the balance and the total interest earned
	cout << "Total number of months needed: " << count << endl;
	cout << "Total amount of interest earned: " << total_interest_paid << endl;
	
	return 0;
}

