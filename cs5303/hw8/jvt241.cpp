//  Jose Tomas Vicuna
//  CS5303 homework #8
//

/*
 I understand that using, receiving or giving unauthorized assistance in writing this assignment is in violation of academic regulations and
 is subject to academic discipline, including a grade of 0 for this assignment with no chance of a making up the assignment, forfeiture of
 credit for the course, probation and dismissal from NYU. By submitting this work I am certifying that I did not cheat!
 */

/*
 Write a C++ program that reads in a text file ( called data8.txt), and prints the file to the screen the text with all extra blanks removed (that is, if there are 2 or more blanks  in a row, replace them by a single blank)  and changes  ALL  letters to UPPERCASE letters.
 
 WATCH THAT YOU DON'T DELETE CARRIAGE RETURNS and tabs. Whitespace includes tabs and carriage returns as well as blanks…so you only want to get rid of extra blank characters.
 
 Hint read in 1 char at a time.
 
 As usual call your program HW8.cpp and submit your program via NYU Classes.
 
 Sample input Text:
 
 In    the    late 60s and      early 70s,       PL/I  was       popular, and    was the largest language of its day. The C language was       developed       as a       reaction, where     the language itself is     relatively small, and instead of the hundreds of "built-in" functions of           PL/I,        it      allowed        the user to      choose the subset of functions they wanted to use via #include statements.
 
 Later, C++ was        developed as an extension to C, creating a        language       that was still procedure-oriented via its functions., but with object                constructions                  overlaid on it.  As C++ continued to develop, more                     constructions                   were added ( e.g. templates),                  and existing                   features were redefined .!
*/

#include <fstream>
#include <cctype>
#include <iostream>

using namespace std;

int main ()
{
    
    ifstream fin;
    char next;
    char next2;
    
    fin.open("data8.txt");
    if(fin.fail())
    {
        cout << "ERROR file could not be read";
    }
    
    fin.get(next);
    
    while(!fin.eof())
    {
        if(isalpha(next)){
            next = toupper(next);
            cout << next;
            fin.get(next);
        }
        
        else if(isspace(next)){
            fin.get(next2);
            if(!isalpha(next2)){
                
                if(next2 == '.'){
                    fin.putback(next2);
                    fin.get(next);
                }
                else{
                    fin.putback(next2);
                    cout << next;
                    do{
                        fin.get(next);
                    }while(isspace(next));
                }
            }
            else{
                fin.putback(next2);
                cout << next;
                do{
                    fin.get(next);
                }while(isspace(next));
            }
        }
        
        else if((!isalpha(next))){
                fin.get(next2);
                if(next == '(' && isspace(next2))
                {
                    cout << next;
                    fin.get(next);
                }

                else if(isspace(next2)){
                    fin.putback(next2);
                    cout << next;
                    fin.get(next);
                }
                else if(isdigit(next2) || (isalpha(next2))){
                    fin.putback(next2);
                    cout << next;
                    fin.get(next);
                }
                else if(next == '.' && next2 == '!'){

                    cout << next;
                    fin.get(next);
                }
                else if(next == '.' && !isspace(next2)){
                    fin.putback(next2);
                    fin.get(next);
                }

        }
    }
    return 0;
}


