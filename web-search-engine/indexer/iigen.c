/*
  iigen - inverted index generator
 */

#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include "lexicon.h"
#include "iindex.h"
#include "utils.h"



/*
 main function of the iigen (Inverted Index Generator)
 */

int main(int argc, char *argv[])
{
  /* argument parsing
      -h help
      -1 phase1: generate lexicons
      -2 phase2: sort lexicons
      -3 phase3: build partial index
      -4 phase4: merge inverted index
      -v verbose
   */

  int phase = 0;
  int verbose = 0;

  char c = '0';
  while ((c = getopt(argc, argv, "1234vb:n:")) != -1)
  {
    switch (c) {
      case '1':
        phase = 1;
        break;
      case '2':
        phase = 2;
        break;
      case '3':
        phase = 3;
        break;
      case '4':
        phase = 4;
        break;
      case 'v':
        verbose = 1;
        break;
      case 'b':
        bzero(BASE_DIR, 256);
        strncpy(BASE_DIR, optarg, 255);
        printf("%s\n", BASE_DIR);
        break;
      case 'n':
        bucket_size = atoi(optarg);
      default:
        printf("invalid argument. please check help...\n");
        exit(1);
    }
  }

  if (*BASE_DIR == '\0') {
    bzero(BASE_DIR, 256);
    strncpy(BASE_DIR, "test_data/", 255);
  }

  if (bucket_size == 0) {
    bucket_size = 10;
  }

  switch(phase){
    case 1:
      lexicon_generator();
      break;

    case 2:
      lexicon_sorter();
      break;

    case 3:
      index_builder();
      break;

    case 4:
      index_merger();
      break;

    default:
      lexicon_generator();
      lexicon_sorter();
      index_builder();
      index_merger();
      break;
  }

  time_t ts;
  time(&ts);
  struct tm * tm = localtime(&ts);
  char timestr[32] = {'\0'};

  snprintf(timestr, 32, "%d-%02d-%02d %02d:%02d:%02d", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec);
  printf("%s Job finished.\n", timestr);
  return 0;
}

