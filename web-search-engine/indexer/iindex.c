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

int initiate_global();
void write_git(int count_in_git, FILE *fdw);
void update_git(int word_id, int offset);
void write_mit(int count_in_mit, FILE *fdw);
void update_mit(int docid, int offset);
void write_iidx(int offset, FILE *fdw, int cprs);


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

int gen_iindex(char *lex_file, char *git_file, char *mit_file, char *iidx_file)
{
  int ret = 0;
  int count_in_git = 0;
  int count_in_mit = 0;
  int offset_in_git = 0;
  int offset_in_mit = 0;

  FILE *f_git = NULL, *f_mit = NULL, *f_iidx = NULL, *f_lex = NULL;
  f_lex = fopen(lex_file, "rb");
  f_git = fopen(git_file, "wb");
  f_mit = fopen(mit_file, "wb");
  f_iidx = fopen(iidx_file, "wb");
  assert(f_lex != NULL && f_git != NULL && f_mit != NULL && f_iidx != NULL);

  while (!feof(f_lex)) {
    ret = fread(cur_lex, sizeof(LEXICON_T), 1, f_lex);
    if (ret == 0) {
      // Write cur_mit, cur_git back;
      write_git(count_in_git, f_git);
      write_mit(count_in_mit, f_mit);
      break;
    }

    // SET OFFSET WHEN CREATE NEW GIT OR MIT, UPDATE COUNT WHEN WRITE BACK TO FILE
    if (cur_lex->word_id != cur_git->word_id) {
      //write cur_git to f_git, update with cur_lec
      write_git(count_in_git, f_git);
      update_git(cur_lex->word_id, offset_in_git);
      count_in_git = 0;

      //write cur_mit to f_mit, update with cur_lec
      write_mit(count_in_mit, f_mit);
      update_mit(cur_lex->docid, offset_in_mit);
      count_in_mit = 0;
      count_in_git++;
      offset_in_git++;

      write_iidx(cur_lex->offset, f_iidx, 0);
      count_in_mit++;
      offset_in_mit++;
 
      continue;
    }

    if (cur_lex->docid != cur_mit->docid) {
      //update count_in_git

      //write cur_mit to f_mit, update with cur_lec 
      write_mit(count_in_mit, f_mit);
      update_mit(cur_lex->docid, offset_in_mit);
      count_in_mit = 0;
      count_in_git++;
      offset_in_git++;

      write_iidx(cur_lex->offset, f_iidx, 0);
      count_in_mit++;
      offset_in_mit++;

      continue;
    }

    if (count_in_mit > 255) {
      continue;
    }

    //update count_in_mit
    write_iidx(cur_lex->offset, f_iidx, 1);
    count_in_mit++;
    offset_in_mit++;
  }

  fclose(f_iidx);
  fclose(f_mit);
  fclose(f_git);
  fclose(f_lex);

  return 0;
}

void write_git(int count_in_git, FILE *fdw){
  if (count_in_git == 0 || cur_git->word_id == 0) {
    return;
  }

  cur_git->n_docs = count_in_git;
  fwrite(cur_git, sizeof(GIT_T), 1, fdw);
  return;
}

void update_git(int word_id, int offset){
  cur_git->word_id = word_id;
  cur_git->offset = offset * sizeof(MIT_T);
  cur_git->n_docs = 0;
  return;
}

void write_mit(int count_in_mit, FILE *fdw){
  if (count_in_mit == 0 || cur_mit->docid == 0) {
    return;
  }

  cur_mit->n_places = count_in_mit;
  fwrite(cur_mit, sizeof(MIT_T), 1, fdw);
  return;
}
void update_mit(int docid, int offset){
  cur_mit->docid = docid;
  cur_mit->offset = offset * sizeof(IIDX_T);
  cur_mit->n_places = 0;
  return;
}

void write_iidx(int offset, FILE *fdw, int cprs){
  if (cprs == 0) {
    cur_iidx->offset = offset;
    fwrite(cur_iidx, sizeof(IIDX_T), 1, fdw);
  } else {
    cur_iidx->offset = offset - cur_iidx->offset;
    fwrite(cur_iidx, sizeof(IIDX_T), 1, fdw);
    cur_iidx->offset = offset;
  }
  return;
}

int index_builder()
{
  int ret = 0;
  int numFile = 0;

  ret = initiate_global();
  if (ret == -1) {
    return EXIT_FAILURE;
  }

  // get file list to process
  char **p = get_inout_filelist(IINDEX_GENERATION);
  char **p_save = p;

  if (p == NULL) {
    return 1;
  }

  while (*p != NULL && *(p+1) != NULL && *(p+2) != NULL && *(p+3) != NULL) {
    gen_iindex(*p, *(p+1), *(p+2), *(p+3));
    numFile++;
    p += 4;
  }

  free_inout_filelist(p_save);
  return 0;
}

int index_merger()
{
  return 0;
}


#ifdef __TEST__
int main(int argc, char * argv[])
{
  return index_builder();
}
#endif

