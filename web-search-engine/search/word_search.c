#include "word_search.h"
#include <time.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <assert.h>
#include <string.h>


static int fd_word_idx = -1;
static int fd_word_str = -1;

static void *p_word_idx_mmap = NULL;
static void *p_word_str_mmap = NULL;


/*
 * load the word index table into memory
 */
static void load_word_idx_table()
{
  static char filename_fd_word_idx[256] = {'\0'};
  static char filename_fd_word_str[256] = {'\0'};

  if (fd_word_idx > 0 && fd_word_str > 0) {
    return;
  }

  bzero(filename_fd_word_idx, 256);
  bzero(filename_fd_word_str, 256);

  strncpy(filename_fd_word_idx, "test_data/tiny30/output/word_table.idx", 256);
  strncpy(filename_fd_word_str, "test_data/tiny30/output/word_table.data", 256);

  fd_word_idx = open(filename_fd_word_idx, O_RDONLY);
  fd_word_str = open(filename_fd_word_str, O_RDONLY);

  assert(fd_word_idx != -1);
  assert(fd_word_str != -1);

  struct stat st1, st2;
  fstat(fd_word_idx, &st1);
  fstat(fd_word_str, &st2);

  p_word_idx_mmap = mmap(NULL, st1.st_size, PROT_READ, MAP_PRIVATE, fd_word_idx, 0);
  assert(p_word_idx_mmap != NULL);
  printf("mapped word index table at %p\n", p_word_idx_mmap);

  p_word_str_mmap = mmap(NULL, st2.st_size, PROT_READ, MAP_PRIVATE, fd_word_str, 0);
  assert(p_word_str_mmap != NULL);
  printf("mapped word data table at %p\n", p_word_str_mmap);

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

