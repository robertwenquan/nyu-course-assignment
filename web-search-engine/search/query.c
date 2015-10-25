#include <stdio.h>
#include "query.h"
#include "pagerank.h"

/*
 * query a single word by word_id
 */
MIT_T **query_word(unsigned int word_id)
{
  printf("word id: %u\n", word_id);

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
}


/*
 * query a list of words based on some logical operation
 */
void query_words(MIT_T *** p_mit_lists, int *word_ids)
{
  /*
   * 1. For each word, find all docs contain this word
   *    Input: list of word ids
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
  while (*word_ids != -1) {
    int word_id = *word_ids;
    printf("word id: %d\n\n", word_id);
    ret_mits = query_word(word_id);
    if (ret_mits == NULL) {
      continue;
    }
    *p_mit_lists = ret_mits;
    word_ids++;
    p_mit_lists++;
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

/*
 * print number list
 * int * = {1, 2, 4, -1}
 * for debugging purpose
 */
void print_number_list(int *nums)
{
  int *p_num = nums;
  while (*p_num != -1) {
    printf("num check: %d\n", *p_num);
    p_num++;
  }
}

/* main routine */
int main(int argc, char *argv[])
{

  /* parse the query keywords */
  char **search_keywords = NULL;
  parse_arguments(argc, argv, &search_keywords);
  printf("Checking query keywords...\n");
  print_string_list(search_keywords);

  /* convert words to word ids */
  int *query_ids = NULL;
  convert_words_to_ids(search_keywords, argc-1, &query_ids);
  printf("Checking query word IDs...\n");
  print_number_list(query_ids);

  URL_IDX_T * p_doc_meta = get_doc_meta(*query_ids);
  print_doc_meta_entry(p_doc_meta);

  /* query word ids, get list of mit entries */
  MIT_T *** p_mit_lists = (MIT_T ***)calloc(argc, sizeof(MIT_T**));
  assert(p_mit_lists != NULL);

  query_words(p_mit_lists, query_ids);

  /*
   * Pass MIT_T *** to ranking_docs get ranked docs
   * DOC_LIST contains docid, with its score and query words offset
   */

  if (p_mit_lists == NULL) {
    return EXIT_FAILURE;
  }

  DOC_LIST * head = ranking_docs(p_mit_lists);

  if (head == NULL) {
    return EXIT_FAILURE;
  }

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

