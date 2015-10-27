#include <stdio.h>
#include "query.h"
#include "pagerank.h"
#include "network.h"

int web_mode = 0;

/*
 * query a single word by word_id
 */
MIT_T **query_word(unsigned int word_id)
{
  if (verbose) {
    printf("word id: %u\n", word_id);
  }

  /* 2. word_id to GIT entry */
  if (verbose) {
    printf("query GIT entry...\n");
  }

  GIT_T *p_git_entry = query_git(word_id);
  if (p_git_entry == NULL) {
    return NULL;
  }
  if (verbose) {
    print_git_entry(p_git_entry);
  }

  /* 3. GIT entry to MIT entry */
  if (verbose == 1) {
    printf("query MIT entry...\n");
  }

  MIT_T **p_mit_entry = query_mit(p_git_entry);
  if (p_mit_entry == NULL) {
    return NULL;
  }

  MIT_T **p_save = p_mit_entry;
  if (verbose) {
    while(*p_mit_entry != NULL){
      print_mit_entry(*p_mit_entry);
      p_mit_entry++;
    }
  }
  p_mit_entry = p_save;

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
   */
  MIT_T ** ret_mits = (MIT_T **)calloc(1, sizeof(MIT_T *));
  while (*word_ids != -1) {
    int word_id = *word_ids;
    ret_mits = query_word(word_id);
    if (ret_mits == NULL) {
      word_ids++;
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
static void parse_arguments(int argc, char *argv[])
{
  // process getopt
  int option = 0;

  while ((option = getopt(argc, argv,"vwb:n:")) != -1) {
    switch (option) {
      case 'v' :
        verbose = 1;
        break;
      case 'w' :
        web_mode = 1;
        break;
      case 'b' :
        bzero(BASE_DIR, 256);
        strncpy(BASE_DIR, optarg, 255);
        break;
      case 'n':
        ndocs_per_lexicon_bucket = atoi(optarg);
        break;
      default:
        printf("arg error!\n");
        exit(EXIT_FAILURE);
    }
  }
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

void process_query(char ** search_keywords, int nwords, int fd)
{

  time_t ts;
  time(&ts);
  struct tm * tm = localtime(&ts);
  char timestr[32] = {'\0'};
  struct timeval tv1;
  gettimeofday(&tv1, NULL);

  snprintf(timestr, 32, "%d-%02d-%02d %02d:%02d:%02d", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec);
  printf("%s started query...\n", timestr);


  /* convert words to word ids */
  int *query_ids = NULL;
  convert_words_to_ids(search_keywords, nwords, &query_ids);
  if (verbose) {
    printf("Checking query word IDs...\n");
    print_number_list(query_ids);
  }

  /* query word ids, get list of mit entries */
  MIT_T *** p_mit_lists = (MIT_T ***)calloc(nwords + 1, sizeof(MIT_T**));
  assert(p_mit_lists != NULL);

  query_words(p_mit_lists, query_ids);
  /*
   * Pass MIT_T *** to ranking_docs get ranked docs
   * DOC_LIST contains docid, with its score and query words offset
   */

  if (*p_mit_lists == NULL) {
    return;
  }
  DOC_LIST * head = ranking_docs(p_mit_lists);
  if (head == NULL) {
    return;
  }

  printf("%d\n", fd);
  fetch_doc_list(head, fd);

  // timer
  struct timeval tv2;
  gettimeofday(&tv2, NULL);

  float diff = 0;
  if (tv2.tv_usec - tv1.tv_usec < 0) {
    diff = tv2.tv_usec - tv1.tv_usec + (tv2.tv_sec - tv1.tv_sec)*1000000;
  }
  else {
    diff = tv2.tv_usec - tv1.tv_usec;
  }
  diff /= 1000.0;

  printf("time spent in query: %.2f ms\n", diff);
}

/*
 * check against blacklist words
 * return 1 if yes
 * return 0 otherwise
 */
static int check_blacklist(char *word)
{
  static char * blacklist_words[] = {
    "are",
    "Are",
    "is",
    "Is",
    "A",
    "a",
    "The",
    "the",
    "an",
    "An",
    "and",
    "And",
    NULL
  };

  char ** p_work = blacklist_words;
  while (*p_work != NULL) {
    if (strcmp(word, *p_work) == 0) {
      return 1;
    }
    p_work++;
  }

  return 0;
}

char **tokenize_input(char *input_line, int *nwords)
{
  char ** keywords = (char **)malloc(sizeof(char **)*(20));
  bzero(keywords, sizeof(char **)*(20));
  assert(keywords != NULL);
  char **p_work = keywords;

  char *p = NULL;
  *nwords = 0;
  for (p = strtok(input_line, " "); p != NULL; p = strtok(NULL, " ")) {

    // strip the trailing '\n'
    char *pos;
    if ((pos=strchr(p, '\n')) != NULL) {
      *pos = '\0';
    }

    // check against blacklist
    if (check_blacklist(p) == 1) {
      continue;
    }

    (*nwords)++;

    *p_work = (char *)malloc(strlen(p) + 1);
    bzero(*p_work, strlen(p) + 1);
    memcpy(*p_work, p, strlen(p));
    p_work++;
  }

  //for (p = strtok(input_line, " "); p != NULL; p = strtok(NULL, " ")) {
  //}

/*

  char **p_work = *keywords;
  int idx = 0;
  for (idx = optind;idx < argc;idx++) {
    *p_work = (char *)malloc(strlen(argv[idx]) + 1);
    bzero(*p_work, strlen(argv[idx]) + 1);
    memcpy(*p_work, argv[idx], strlen(argv[idx]));
    p_work++;
  }
  p_work = NULL;
*/

  return keywords;
}

/* main routine */
int main(int argc, char *argv[])
{
  // argument parsing
  parse_arguments(argc, argv);

  /* load config */
  load_config();

  /* parse the query keywords */
  char **search_keywords = NULL;

  /* enter web mode when -w is set */
  if (web_mode == 1) {
    start_server();
  }

  /* read lines from STDIN and goes to loop */
  printf("Enter your query terms (Ctrl-C to exit): ");
  char *line = NULL;
  size_t size;
  while (getline(&line, &size, stdin) != -1) {
    if (verbose) {
      printf("input: %s", line);
    }
    int nwords = 0;
    search_keywords = tokenize_input(line, &nwords);
    if (verbose) {
      printf("Checking query keywords...\n");
      print_string_list(search_keywords);
    }

    if (search_keywords != NULL) {
      process_query(search_keywords, nwords, STDOUT_FILENO);
    }
    printf("\nEnter your query terms (Ctrl-C to exit): ");
  }

  return 0;
}

