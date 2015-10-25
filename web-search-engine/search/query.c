#include <stdio.h>
#include "query.h"
#include "pagerank.h"
/*
 * query a single word
 */
MIT_T **query_word(char *word)
{
  /* 1. word to word_id */
  printf("query word_id for %s\n", word);
  int word_id = -1;
  word_id = word_to_id(word);
  if (word_id < 0) {
    return NULL;
  }

  printf("word id: %d\n", word_id);

  /* 2. word_id to GIT entry */
  printf("query GIT entry...\n");
  GIT_T *p_git_entry = query_git(word_id);
  if (p_git_entry == NULL) {
    return NULL;
  }
  print_git_entry(p_git_entry);

  /* 3. GIT entry to MIT entry */
  printf("query MIT entry...\n");
  MIT_T **p_mit_entry = query_mit(p_git_entry);
  if (p_mit_entry == NULL) {
    return NULL;
  }
  MIT_T **p_save = p_mit_entry;
  while(*p_mit_entry != NULL){
    print_mit_entry(*p_mit_entry);
    p_mit_entry++;
  }
  p_mit_entry = p_save;


  /* 4. MIT entry to IINDEX entry */
  printf("query IINDEX entry...\n");

  IIDX_T * p_iidx_entry = NULL;
  int i = 0;
  while(*p_mit_entry != NULL){
    //p_iidx_entry = query_compressed_iindex(*p_mit_entry);
    p_iidx_entry = query_iindex(*p_mit_entry);
    if (p_iidx_entry == NULL) {
      return NULL;
    }
    i = 0;
    while(p_iidx_entry[i].offset != -1 ){
      print_iidx_entry(&p_iidx_entry[i]);
      i++;
    }

    p_mit_entry++;
  }

  return p_save;

  /* 5. IINDEX entry to WARC info */

  /* 6. WARC info to page text */
}


/*
 * query a list of words based on some logical operation
 */
void query_words(MIT_T *** p_mit_lists, char ** search_keywords)
{
  /*
   * 1. For each word, find all docs contain this word
   *    Input: list of words
   *    Output: MIT_T ***
   *
   * 2. Union docs for all words
   *    Input: MIT_T ***
   *    Output : int * list_docs
   *
   * 3. Cal BM25 of each doc
   *    Input: doc, queries[]
   *    Output: BM25
   *
   * 4. Return top 20 docs with context
   */
  MIT_T ** ret_mits = (MIT_T **)calloc(1, sizeof(MIT_T *));
  while (*search_keywords != NULL) {
    printf("keywords: %s\n\n", *search_keywords);
    ret_mits = query_word(*search_keywords);
    if (ret_mits == NULL) {
      continue;
    }
    *p_mit_lists = ret_mits;
    search_keywords++;
    p_mit_lists ++;
  }
  p_mit_lists = NULL;
}


/*
 * parse search keywords from the command line
 */
static void parse_arguments(int argc, char *argv[], char ***keywords)
{
  *keywords = (char **)malloc(sizeof(char **)*argc);
  bzero(*keywords, sizeof(char **)*argc);
  assert(*keywords != NULL);

  char **p_work = *keywords;
  int idx = 0;
  for (idx = 1;idx < argc;idx++) {
    *p_work = (char *)malloc(strlen(argv[idx]) + 1);
    bzero(*p_work, strlen(argv[idx]) + 1);
    memcpy(*p_work, argv[idx], strlen(argv[idx]));
    p_work++;
  }
  p_work = NULL;
}

/*
 * print string list
 * char *[] = {"xxx", "xxx", NULL}
 * for debugging purpose
 */
void print_string_list(char *strlist[])
{
  char **p_work = (char **)strlist;
  while (*p_work != NULL) {
    printf("str check: %s\n", *p_work);
    p_work++;
  }
}

/* main routine */
int main(int argc, char *argv[])
{

  /* parse the query keywords */
  char **search_keywords = NULL;
  parse_arguments(argc, argv, &search_keywords);
  print_string_list(search_keywords);

  /* query keywords, get list of mit entries */

  MIT_T *** p_mit_lists = (MIT_T ***)calloc(argc, sizeof(MIT_T**));
  assert(p_mit_lists != NULL);

  query_words(p_mit_lists, search_keywords);

  /*
   * Pass MIT_T *** to ranking_docs get ranked docs
   * DOC_LIST contains docid, with its score and query words offset
   */

  DOC_LIST * head = ranking_docs(p_mit_lists);

  /* USED FOR TEST
  DOC_LIST * cur = head;
  while(cur != NULL) {
    if (cur->docid == -1 ){
      break;
    }
    printf("docid: %d\n", cur->docid);
    printf("score : %f\n", cur->score);
    printf("offset : %d\n", cur->offsets[0]);

    cur++;
  }
  */
  /*
   * Get context according to DOC_LIST and return
   */

  return 0;
}

