#include "word_search.h"
#include <time.h>
#include <stdlib.h>


static int fd_word_idx = -1;
static int fd_word_str = -1;

static void *p_word_idx_mmap = NULL;
static void *p_word_str_mmap = NULL;


/*
 * load the word index table into memory
 */
static void load_word_idx_table()
{
  fd_word_idx = 33;
  fd_word_str = 34;

  p_word_idx_mmap = NULL;
  p_word_str_mmap = NULL;

  return;
}


/*
 * release all relevant memory for the word index table
 */
static void close_word_idx_table()
{
  return;
}


/*
 * query word id from the word_id index table
 * input: word as a string
 * output: word_id if it exists
 */
int word_to_id(char *word)
{
  // initialize everything when necessary
  if (fd_word_idx == -1 && fd_word_str == -1) {
    load_word_idx_table();
  }

  // generate a random word_id from 33 to 35
  srand(time(NULL));
  int random_wordid = rand() % 3 + 33;

  close_word_idx_table();

  return random_wordid;
}

