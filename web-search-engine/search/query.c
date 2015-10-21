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

  /* 3. GIT entry to MIT entry */

  /* 4. MIT entry to IINDEX entry */

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

