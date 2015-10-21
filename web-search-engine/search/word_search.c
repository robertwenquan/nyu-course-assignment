#include "word_search.h"
#include <time.h>
#include <stdlib.h>


/*
 * query word id from the word_id index table
 * input: word as a string
 * output: word_id if it exists
 */
int word_to_id(char *word)
{
  // generate a random word_id from 33 to 35
  srand(time(NULL));
  int random_wordid = rand() % 3 + 33;
  return random_wordid;
}

