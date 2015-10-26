#include "word_search.h"
#include <time.h>
#include <fcntl.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <sys/mman.h>
#include <assert.h>
#include <pthread.h>
#include <string.h>


static int fd_word_idx = -1;
static int fd_word_str = -1;

static void *p_word_idx_mmap = NULL;
static void *p_word_str_mmap = NULL;

static WORDID_HASHTREE_NODE_T wordid_hash_root;

/*
 * get the word string representatio in a prepared buffer
 * with the word_id and the offset
 */
void get_word_str(WORD_IDX_T *p_word_idx, char *wordstr, int lens)
{
  unsigned int offset = p_word_idx->offset;
  unsigned short word_lens = p_word_idx->length;

  char *p_word_start = (char *)p_word_str_mmap + offset;
  bzero(wordstr, lens);
  memcpy(wordstr, p_word_start, word_lens);
}

/*
 * load one word into the hash tree
 * for word->id query
 */
static void load_word(int word_id, char *word)
{
  static int wordid = 0;
  static pthread_mutex_t wordid_lock;

  int word_lens = strlen(word);

  WORDID_HASHTREE_NODE_T *work_node = &wordid_hash_root;

  int idx = 0;
  for (idx=0;idx<word_lens;idx++) {
    char chr = word[idx];
    int node_idx = char_to_index(chr);
    assert(node_idx >= 0 && node_idx < 62);

    WORDID_HASHTREE_NODE_T *tree_node = work_node->next[node_idx];
    if (tree_node == NULL) {
      tree_node = (WORDID_HASHTREE_NODE_T *)malloc(sizeof(WORDID_HASHTREE_NODE_T));
      if (tree_node == NULL) {
        return;
      }
      memset(tree_node, 0, sizeof(WORDID_HASHTREE_NODE_T));

      tree_node->chr = chr;
      tree_node->wordid = 0;

      pthread_mutex_lock(&wordid_lock);
      work_node->next[node_idx] = tree_node;
      pthread_mutex_unlock(&wordid_lock);
    }

    work_node = tree_node;
  }

  // at this point, work_node points to the last node
  if (work_node->wordid == 0) {
    wordid++;
    pthread_mutex_lock(&wordid_lock);
    work_node->wordid = wordid;
    pthread_mutex_unlock(&wordid_lock);
  }

  //assert(work_node->wordid == word_id);
}

/*
 * load the word index table into memory
 */
static void load_word_idx_table()
{
  static char filename_fd_word_idx[256] = {'\0'};
  static char filename_fd_word_str[256] = {'\0'};

  if (fd_word_idx > 0 && fd_word_str > 0) {
    return;
  }

  bzero(filename_fd_word_idx, 256);
  bzero(filename_fd_word_str, 256);

  snprintf(filename_fd_word_idx, 256, "%s/output/word_table.idx", get_basedir());
  snprintf(filename_fd_word_str, 256, "%s/output/word_table.data", get_basedir());

  fd_word_idx = open(filename_fd_word_idx, O_RDONLY);
  fd_word_str = open(filename_fd_word_str, O_RDONLY);

  assert(fd_word_idx != -1);
  assert(fd_word_str != -1);

  struct stat st1, st2;
  fstat(fd_word_idx, &st1);
  fstat(fd_word_str, &st2);

  p_word_idx_mmap = mmap(NULL, st1.st_size, PROT_READ, MAP_PRIVATE, fd_word_idx, 0);
  assert(p_word_idx_mmap != NULL);
  printf("mapped word index table at %p\n", p_word_idx_mmap);

  p_word_str_mmap = mmap(NULL, st2.st_size, PROT_READ, MAP_PRIVATE, fd_word_str, 0);
  assert(p_word_str_mmap != NULL);
  printf("mapped word data table at %p\n", p_word_str_mmap);

  int nwords = st1.st_size/sizeof(WORD_IDX_T);
  int idx = 0;
  char wordstr[256] = {'\0'};
  bzero(wordstr, 256);
  WORD_IDX_T *p_word_idx = NULL;

  for (idx = 0;idx<nwords;idx++) {
    p_word_idx = (WORD_IDX_T *)p_word_idx_mmap + idx;
    get_word_str(p_word_idx, wordstr, 256);
    load_word(p_word_idx->word_id, wordstr);
  }

  close(fd_word_idx);
  close(fd_word_str);

  return;
}


static unsigned int query_word_for_id(char *word)
{
  int word_lens = strlen(word);

  WORDID_HASHTREE_NODE_T *work_node = &wordid_hash_root;

  int idx = 0;
  for (idx=0;idx<word_lens;idx++) {
    char chr = word[idx];
    int node_idx = char_to_index(chr);
    assert(node_idx >= 0 && node_idx < 62);

    WORDID_HASHTREE_NODE_T *tree_node = work_node->next[node_idx];
    if (tree_node == NULL) {
      return -1;
    }
    work_node = tree_node;
  }

  return work_node->wordid;
}


/*
 * release all relevant memory for the word index table
 */
static void close_word_idx_table()
{
  return;
}

/*
 * query word id from the word_id index table
 * input: word as a string
 * output: word_id if it exists
 */
int word_to_id(char *word)
{
  // initialize everything when necessary
  if (fd_word_idx == -1 && fd_word_str == -1) {
    load_word_idx_table();
  }

  return query_word_for_id(word);
}

/*
 * convert word list to word_id list
 * input: a list of words
 *   {"new", "york", NULL}
 * output:
 *   {123, 234, -1}
 */
void convert_words_to_ids(char **search_keywords, int nwords, int **ids)
{
  *ids = (int *)malloc(sizeof(int) * (nwords+1));
  assert(*ids != NULL);
  
  char **p_word = search_keywords;
  int *p_int = *ids;
  while (*p_word != NULL) {
    int word_id = word_to_id(*p_word);
    if (word_id != -1) {
      *p_int = word_to_id(*p_word);
      p_int++;
    }
    p_word++;
  }
  *p_int = -1;
}

