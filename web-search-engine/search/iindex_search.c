#include "iindex_search.h"
/*
 * query GIT entry based on the word_id
 * input: word id
 * output: an GIT_T entry in the GIT index table
 */
GIT_T * query_git(int word_id)
{
  // Open *.git file and find word_id using binary search
  //char **p = get_inout_filelist(IINDEX_MERGING);
  FILE * f_git;
  int v_check = 0;

  f_git = fopen("../indexer/test_data/output/input1.warc.wet.lexicon00.git", "rb");
  if (f_git == NULL) {
    return NULL;
  }

  GIT_T * ret = (GIT_T *)malloc(sizeof(GIT_T));

  while (!feof(f_git)) {
    v_check = fread(ret, sizeof(GIT_T), 1, f_git);

    if (v_check == 0) {
      fclose(f_git);
      return NULL;
    }

    if (ret->word_id == word_id) {
      fclose(f_git);
      return ret;
    }

    if (ret->word_id > word_id) {
      fclose(f_git);
      return NULL;
    }
  } 

  fclose(f_git);
  return NULL;
}


/*
 * query MIT entry based on the offset and length
 * input: GIT_T entry
 * output: MIT_T entry
 */
MIT_T * query_mit(GIT_T *p_git)
{
  // Open *.mit file, return a list of MIT_T entries
  printf("JUST TEST");
  if (p_git == NULL) {
    return NULL;
  }

  return NULL;
}

/*
 * query inverted index based on the offset and length
 * input: MIT_T entry
 * output: inverted index list
 */
void * query_iindex(MIT_T *p_mit)
{
  printf("JUST TEST");
  // Open corresponding .iidx file and return a list of offset
  return NULL;
}
