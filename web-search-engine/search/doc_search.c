#include "doc_search.h"
#include <time.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <assert.h>
#include <string.h>


static int fd_url_idx = -1;
static int fd_url_str = -1;

static void *p_url_idx_mmap = NULL;
static void *p_url_str_mmap = NULL;


/*
 * load the url index table into memory
 */
static void load_url_idx_table()
{
  static char filename_fd_url_idx[256] = {'\0'};
  static char filename_fd_url_str[256] = {'\0'};

  if (fd_url_idx > 0 && fd_url_str > 0) {
    return;
  }

  bzero(filename_fd_url_idx, 256);
  bzero(filename_fd_url_str, 256);

  strncpy(filename_fd_url_idx, "test_data/tiny30/output/url_table.idx", 256);
  strncpy(filename_fd_url_str, "test_data/tiny30/output/url_table.data", 256);

  fd_url_idx = open(filename_fd_url_idx, O_RDONLY);
  fd_url_str = open(filename_fd_url_str, O_RDONLY);

  assert(fd_url_idx != -1);
  assert(fd_url_str != -1);

  struct stat st1, st2;
  fstat(fd_url_idx, &st1);
  fstat(fd_url_str, &st2);

  p_url_idx_mmap = mmap(NULL, st1.st_size, PROT_READ, MAP_PRIVATE, fd_url_idx, 0);
  assert(p_url_idx_mmap != NULL);
  printf("mapped url index table at %p\n", p_url_idx_mmap);

  p_url_str_mmap = mmap(NULL, st2.st_size, PROT_READ, MAP_PRIVATE, fd_url_str, 0);
  assert(p_url_str_mmap != NULL);
  printf("mapped url data table at %p\n", p_url_str_mmap);

  return;
}


/*
 * release all relevant memory for the url index table
 */
static void close_url_idx_table()
{
  return;
}


/*
 * query doc meta info from docid
 * input: docid
 * output: doc meta structure
 */
int fetch_doc_meta(int docid)
{
  // initialize everything when necessary
  if (fd_url_idx == -1 && fd_url_str == -1) {
    load_url_idx_table();
  }

  close_url_idx_table();

  return 0;
}

