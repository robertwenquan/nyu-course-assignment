#include <stdio.h>
#include "query.h"

/*
 * query a single word
 */
void query_word(char *word)
{
  /* 1. word to word_id */
  printf("query word_id for %s\n", word);
  int word_id = -1;
  word_id = word_to_id(word);
  if (word_id < 0) {
    return;
  }

  printf("word id: %d\n", word_id);

  /* 2. word_id to GIT entry */
  printf("query GIT entry...\n");
  GIT_T *p_git_entry = query_git(word_id);
  if (p_git_entry == NULL) {
    return;
  }
  print_git_entry(p_git_entry);

  /* 3. GIT entry to MIT entry */
  printf("query MIT entry...\n");
  MIT_T **p_mit_entry = query_mit(p_git_entry);
  if (p_mit_entry == NULL) {
    return;
  }
  MIT_T **p_save = p_mit_entry;
  while(*p_mit_entry != NULL){
    print_mit_entry(*p_mit_entry);
    p_mit_entry++;
  }
  p_mit_entry = p_save;

  /* 4. MIT entry to IINDEX entry */
  printf("query IINDEX entry...\n");

  IIDX_T * p_iidx_entry = (IIDX_T *) calloc (1024, sizeof(IIDX_T *));
  int i = 0;
  while(*p_mit_entry != NULL){
    p_iidx_entry = query_iindex(*p_mit_entry);
    if (p_iidx_entry == NULL) {
      return;
    }
    i = 0;
    while(p_iidx_entry[i].offset != 0 ){
      print_iidx_entry(&p_iidx_entry[i]);
      i++;
    }

    p_mit_entry++;
  }

  /* 5. IINDEX entry to WARC info */

  /* 6. WARC info to page text */
}


/*
 * query a list of words based on some logical operation
 */
void query_words(char *queries[])
{
  char *word = "cat";
  query_word(word);
}


/* main routine */
int main(int argc, char *argv[])
{
  query_word("fake");

  return 0;
}

