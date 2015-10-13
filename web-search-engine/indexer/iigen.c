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
  while ((c = getopt(argc, argv, "1234vb:")) != -1)
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
      default:
        printf("invalid argument. please check help...\n");
        exit(1);
    }
  }

  switch(phase){
    case 1:
      lexicon_generator();
      break;

    case 2:
      printf("[fake] sorting lexicons...\n");
      break;

    case 3:
      index_builder();
      break;

    case 4:
      index_merger();
      break;

    default:
      lexicon_generator();
      index_builder();
      index_merger();
      break;
  }

  return 0;
}

