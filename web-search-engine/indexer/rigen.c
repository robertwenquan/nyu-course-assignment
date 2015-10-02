/*
  rigen - reversed index generator
 */

#include <stdio.h>
#include <stdlib.h>
#include "lexicon.h"

extern int lexicon_generator();
extern int lexicon_sorter();
extern int index_builder();
extern int index_merger();

/*
 main function of the rigen (Reversed Index Generator)
 */

int main(int argc, char *argv[])
{
  // print welcome information of the indexer
  printf("Let's build the Reversed Index in C!\n");

  /* argument parsing
      -h help
      -1 phase1: generate lexicons
      -2 phase2: sort lexicons
      -3 phase3: build partial index
      -4 phase4: merge reversed index
      -v verbose
   */

  int phase = 0;

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

  return 0;
}

