/**************************************************************************/
/* usage  ./iindex finlist outfileprefix                                  */
/*                                                                        */
/*        finlist        : name of file containing a list of input files  */
/*        outfileprefex  : directory to record intermediate files         */
/*                                                                        */
/* For example:                                                           */
/*          ./merge finlist fout                                          */
/**************************************************************************/

#include <stdio.h>
#include "iindex.h"
#include "utils.h"
#include "lexicon.h"

GIT_T * cur_git;
MIT_T * cur_mit;
IIDX_T * cur_iidx;
LEXICON_T * cur_lex;

static void print_help(char * argv[]);
int initiate_global();

static void print_help(char *argv[]) {
  printf("Help.\n");
  printf(" %s <finlist> <outputfileprefix>\n", argv[0]);
  printf("\n");
  printf("For example:\n");
  printf(" %s finlist ./phase3/fout\n", argv[0]);
}

int initiate_global(){
  cur_git = (GIT_T *)malloc(sizeof(GIT_T));
  if (cur_git == NULL) {
    return -1;
  }
  memset(cur_git, 0, sizeof(GIT_T));

  cur_mit = (MIT_T *)malloc(sizeof(MIT_T));
  if (cur_mit == NULL) {
    return -1;
  }
  memset(cur_mit, 0, sizeof(GIT_T));

  cur_iidx = (IIDX_T *)malloc(sizeof(IIDX_T));
  if (cur_iidx == NULL) {
    return -1;
  }
  memset(cur_iidx, 0, sizeof(IIDX_T));

  cur_lex = (LEXICON_T *)malloc(sizeof(LEXICON_T));
  if (cur_lex == NULL) {
    return -1;
  }
  memset(cur_lex, 0, sizeof(LEXICON_T));

  return 0;
}

int index_builder()
{
  return 0;
}

int index_merger()
{
  return 0;
}


#ifdef __TEST__
int main(int argc, char * argv[])
{
  index_builder();

  int ret = 0;
  if (argc != 3) {
    print_help(argv);
    return EXIT_FAILURE;
  }

  ret = initiate_global();
  if (ret == -1) {
    return EXIT_FAILURE;
  }

  return EXIT_SUCCESS;
}
#endif

