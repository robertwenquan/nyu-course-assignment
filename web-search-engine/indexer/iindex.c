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
FILE *f_git = NULL, *f_mit = NULL, *f_iidx = NULL, *f_lex = NULL;

static void print_help(char * argv[]);
int initiate_global();
void write_git(int count_in_git);
void update_git(int word_id, int offset);
void write_mit(int count_in_mit);
void update_mit(int docid, int offset);
void write_iidx(int offset);

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

int gen_iindex()
{
  int ret = 0;
  int count_in_git = 0;
  int count_in_mit = 0;
  int offset_in_git = 0;
  int offset_in_mit = 0;

  while (!feof(f_lex)) {
    ret = fread(cur_lex, sizeof(LEXICON_T), 1, f_lex);
    if (ret == 0) {
      // Write cur_mit, cur_git back;
      write_git(count_in_git);
      write_mit(count_in_mit);
      break;
    }

    // SET OFFSET WHEN CREATE NEW GIT OR MIT, UPDATE COUNT WHEN WRITE BACK TO FILE
    if (cur_lex->word_id != cur_git->word_id) {
      //write cur_git to f_git, update with cur_lec
      write_git(count_in_git);
      update_git(cur_lex->word_id, offset_in_git);
      count_in_git = 0;

      //write cur_mit to f_mit, update with cur_lec
      write_mit(count_in_mit);
      update_mit(cur_lex->docid, offset_in_mit);
      count_in_mit = 0;
      count_in_git++;
      offset_in_git++;

      write_iidx(cur_lex->offset);
      count_in_mit++;
      offset_in_mit++;
 
      continue;
    }

    if (cur_lex->docid != cur_mit->docid) {
      //update count_in_git

      //write cur_mit to f_mit, update with cur_lec 
      write_mit(count_in_mit);
      update_mit(cur_lex->docid, offset_in_mit);
      count_in_mit = 0;
      count_in_git++;
      offset_in_git++;

      write_iidx(cur_lex->offset);
      count_in_mit++;
      offset_in_mit++;

      continue;
    }

    if (count_in_mit > 255) {
      continue;
    }

    //update count_in_mit
    write_iidx(cur_lex->offset);
    count_in_mit++;
    offset_in_mit++;
  }
  return 0;
}

void write_git(int count_in_git){
  if (count_in_git == 0 || cur_git->word_id == 0) {
    return;
  }

  cur_git->n_docs = count_in_git;
  fwrite(cur_git, sizeof(GIT_T), 1, f_git);
  return;
}

void update_git(int word_id, int offset){
  cur_git->word_id = word_id;
  cur_git->offset = offset * sizeof(MIT_T);
  cur_git->n_docs = 0;
  return;
}

void write_mit(int count_in_mit){
  if (count_in_mit == 0 || cur_mit->docid == 0) {
    return;
  }

  cur_mit->n_places = count_in_mit;
  fwrite(cur_mit, sizeof(MIT_T), 1, f_mit);
  return;
}
void update_mit(int docid, int offset){
  cur_mit->docid = docid;
  cur_mit->offset = offset * sizeof(IIDX_T);
  cur_mit->n_places = 0;
  return;
}

void write_iidx(int offset){
  cur_iidx->offset = offset;
  fwrite(cur_iidx, sizeof(LEXICON_T), 1, f_iidx);
  return;
}

int index_builder(){
  return 0;
}
int index_merger()
{
  return 0;
}
#ifdef __TEST__
int main(int argc, char * argv[])
{
  int ret = 0;
  int numFile = 0;
  char inputlist[1024] = {'\0'};
  char filename[1024] = {'\0'};
  char outprefix[1024] = {'\0'};
  FILE * fin;

  if (argc != 3) {
    print_help(argv);
    return EXIT_FAILURE;
  }

  ret = initiate_global();
  if (ret == -1) {
    return EXIT_FAILURE;
  }

  if (argc != 3) {
    print_help(argv);
    return EXIT_FAILURE;
  }

  ret = initiate_global();
  if (ret == -1) {
    return EXIT_FAILURE;
  }

  strcpy(inputlist, argv[1]);

  fin = fopen(inputlist, "r");
  if (fin == NULL) {
    printf("Open file %s failed", inputlist);
    return EXIT_FAILURE;
  }

  while (!feof(fin)) {
    ret = fscanf(fin, "%s", filename);
    if(feof(fin)){
      break;
    }
    if (ret == -1) {
      return EXIT_FAILURE;
    }

    f_lex = fopen(filename, "r");
    if (f_lex == NULL) {
      return EXIT_FAILURE;
    }

    sprintf(outprefix, "%s%d", argv[2], numFile);

    sprintf(filename, "%s%s", outprefix, ".git");
    f_git = fopen(filename, "w");
    if (f_git == NULL) {
      return EXIT_FAILURE;
    }

    sprintf(filename, "%s%s", outprefix, ".mit");
    f_mit = fopen(filename, "w");
    if (f_mit == NULL) {
      return EXIT_FAILURE;
    }

    sprintf(filename, "%s%s", outprefix, ".iidx");
    f_iidx = fopen(filename, "w");
    if (f_iidx == NULL) {
      return EXIT_FAILURE;
    }

    gen_iindex();
    fclose(f_iidx);
    fclose(f_mit);
    fclose(f_git);
    fclose(f_lex);

    numFile++;
  }
  return EXIT_SUCCESS;
}
#endif

