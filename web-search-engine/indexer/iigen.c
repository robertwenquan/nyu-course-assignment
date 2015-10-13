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

  switch(phase){
    case 1:
      lexicon_generator();
      break;

    case 2:
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

