#include "iindex_search.h"

/*
 * query GIT entry based on the word_id
 * input: word id
 * output: an GIT_T entry in the GIT index table
 */
GIT_T * query_git(int word_id)
{
  return NULL;
}


/*
 * query MIT entry based on the offset and length
 * input: GIT_T entry
 * output: MIT_T entry
 */
MIT_T * query_mit(GIT_T *p_git)
{
  return NULL;
}

/*
 * query inverted index based on the offset and length
 * input: MIT_T entry
 * output: inverted index list
 */
void * query_iindex(MIT_T *p_mit)
{
  return NULL;
}

