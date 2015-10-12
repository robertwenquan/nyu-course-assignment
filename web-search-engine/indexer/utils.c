/*
 utility functions for the inverted index generator

  - gzip helper functions
  - logging functions
   * credit from https://github.com/drfeelngood/logger/

 */

#include <stdio.h>
#include "utils.h"

void * uncompress(char *filename)
{
  return NULL;
}

LOGGER_T * logger_create(void)
{
  LOGGER_T *l = (LOGGER_T *)malloc(sizeof(LOGGER_T));
  if ( l == NULL ) {
    return NULL;
  }

  l->datetime_format = (char *)"%Y-%m-%d %H:%M:%S";
  l->level = LOG_INFO;
  l->fp = stdout;

  return l;
}

void logger_free(LOGGER_T *l)
{
  if (l != NULL) {
    if ( fileno(l->fp) != STDOUT_FILENO ) {
      fclose(l->fp);
    }
    free(l);
  }
}

void log_add(LOGGER_T *l, int level, const char *msg)
{
  if (level < l->level) return;

  time_t meow = time(NULL);
  char buf[64];

  strftime(buf, sizeof(buf), l->datetime_format, localtime(&meow));
  fprintf(l->fp, "[%d] %c, %s : %s\n",
          (int)getpid(),
          LOG_LEVEL_CHARS[level],
          buf,
          msg);
}

void log_debug(LOGGER_T *l, const char *fmt, ...)
{
  va_list ap;
  char msg[LOG_MAX_MSG_LEN];

  va_start(ap, fmt);
  vsnprintf(msg, sizeof(msg), fmt, ap);
  log_add(l, LOG_DEBUG, msg);
  va_end(ap);
}

void log_info(LOGGER_T *l, const char *fmt, ...)
{
  va_list ap;
  char msg[LOG_MAX_MSG_LEN];

  va_start(ap, fmt);
  vsnprintf(msg, sizeof(msg), fmt, ap);
  log_add(l, LOG_INFO, msg);
  va_end(ap);
}

void log_warn(LOGGER_T *l, const char *fmt, ...)
{
  va_list ap;
  char msg[LOG_MAX_MSG_LEN];

  va_start(ap, fmt);
  vsnprintf(msg, sizeof(msg), fmt, ap);
  log_add(l, LOG_WARN, msg);
  va_end(ap);
}

void log_error(LOGGER_T *l, const char *fmt, ...)
{
  va_list ap;
  char msg[LOG_MAX_MSG_LEN];

  va_start(ap, fmt);
  vsnprintf(msg, sizeof(msg), fmt, ap);
  log_add(l, LOG_ERROR, msg);
  va_end(ap);
}

/*
 * docid generator
 */
unsigned int get_doc_id()
{
  static int docid = 0;

  docid++;
  return docid;
}

WORDID_HASHTREE_NODE_T wordid_hash_root;

/*
 * char to index for word id hash sub-tree query
 */
static int char_to_index(char chr)
{
  if (chr >= '0' && chr <= '9') {
    return chr-48;
  } else if (chr >= 'A' && chr <= 'Z') {
    return chr-65+10;
  } else if (chr >= 'a' && chr <= 'z') {
    return chr-97+36;
  } else {
    return -1;
  }
}

/*
 * query from word dictionary
 * return wordid if exists
 * return 0 otherwise
 */
static unsigned int query_word_for_id(char *word)
{
  static int wordid = 0;
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
        return 0;
      }
      memset(tree_node, 0, sizeof(WORDID_HASHTREE_NODE_T));

      tree_node->chr = chr;
      tree_node->wordid = 0;
      work_node->next[node_idx] = tree_node;
    }

    work_node = tree_node;
  }

  // at this point, work_node points to the last node
  if (work_node->wordid == 0) {
    wordid++;
    work_node->wordid = wordid;
  }

  return work_node->wordid;
}

/*
 * wordid generator
 */
unsigned int get_word_id(char *word)
{
  return query_word_for_id(word);
}

