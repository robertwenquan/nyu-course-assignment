/*
 utility functions for the inverted index generator

  - gzip helper functions
  - logging functions
   * credit from https://github.com/drfeelngood/logger/

 */

#include <stdio.h>
#include <glob.h>
#include <pthread.h>
#include "utils.h"

char BASE_DIR[] = "/data/wse/100k/";
//char BASE_DIR[] = "test_data/";

char * get_basedir()
{
  return BASE_DIR;
}

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
unsigned int get_doc_id(WARC_REC_T *p_warc)
{
  static int docid = -1;
  static pthread_mutex_t docid_lock;

  static char filename_url_idx_table[256] = {'\0'};
  static char filename_url_str_table[256] = {'\0'};
  static FILE *fp_url_idx_table = NULL;
  static FILE *fp_url_str_table = NULL;

  if (fp_url_idx_table == NULL && fp_url_str_table == NULL) {
    bzero(filename_url_idx_table, 256);
    bzero(filename_url_str_table, 256);
    snprintf(filename_url_idx_table, 256, "%s%s", BASE_DIR, "output/url_table.idx");
    snprintf(filename_url_str_table, 256, "%s%s", BASE_DIR, "output/url_table.data");
    fp_url_idx_table = fopen(filename_url_idx_table, "wb");
    fp_url_str_table = fopen(filename_url_str_table, "wb");
  }

  int url_lens = strlen(p_warc->header->url);

  pthread_mutex_lock(&docid_lock);
  docid++;

  // write the new (wordid,word) mapping into index table
  URL_IDX_T docid_idx_entry = {.docid = docid,
                               .url_fileid = 0,
                               .url_offset = ftell(fp_url_str_table),
                               .url_length = url_lens,
                               .doc_fileid = 0,
                               .doc_offset = p_warc->offset,
                               .doc_length = p_warc->header->length + p_warc->payload->length,
                               .content_offset = p_warc->header->length,
                               .content_length = p_warc->payload->length,
                              };
  fwrite(&docid_idx_entry, sizeof(URL_IDX_T), 1, fp_url_idx_table);
  fwrite(p_warc->header->url, url_lens, 1, fp_url_str_table);

  pthread_mutex_unlock(&docid_lock);

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
  static pthread_mutex_t wordid_lock;

  static char filename_word_idx_table[256] = {'\0'};
  static char filename_word_str_table[256] = {'\0'};
  static FILE *fp_word_idx_table = NULL;
  static FILE *fp_word_str_table = NULL;

  if (fp_word_idx_table == NULL && fp_word_str_table == NULL) {
    bzero(filename_word_idx_table, 256);
    bzero(filename_word_str_table, 256);
    snprintf(filename_word_idx_table, 256, "%s%s", BASE_DIR, "output/word_table.idx");
    snprintf(filename_word_str_table, 256, "%s%s", BASE_DIR, "output/word_table.data");
    fp_word_idx_table = fopen(filename_word_idx_table, "wb");
    fp_word_str_table = fopen(filename_word_str_table, "wb");
  }

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

      pthread_mutex_lock(&wordid_lock);
      // set the new node_idx
      work_node->next[node_idx] = tree_node;
      pthread_mutex_unlock(&wordid_lock);
    }

    work_node = tree_node;
  }

  // at this point, work_node points to the last node
  // for any new node, the wordid is not assigned so it's 0
  if (work_node->wordid == 0) {
    wordid++;

    pthread_mutex_lock(&wordid_lock);
    work_node->wordid = wordid;

    // write the new (wordid,word) mapping into index table
    WORD_IDX_T wordid_idx_entry = {.word_id = wordid,
                                   .offset = ftell(fp_word_str_table),
                                   .length = word_lens
                                  };
    fwrite(&wordid_idx_entry, sizeof(WORD_IDX_T), 1, fp_word_idx_table);
    fwrite(word, word_lens, 1, fp_word_str_table);

    pthread_mutex_unlock(&wordid_lock);
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

/*
 * get input file list to work on for lexicon generation
 *
 * input will be in ${BASE_DIR}/input/ *.wet
 * output will be in ${BASE_DIR}/output/ *.lexicon
 *
 * return value:
 *  an array of char * with full path filenames
 *    two filenames are in a group
 *    [input1, output1, input2, output2, input3, output3, ...]
 */
char ** get_inout_filelist(PHASE_T phase)
{
  // set input path
  char input_dir[256] = {'\0'};
  if (phase == LEXICON_GENERATION) {
    snprintf(input_dir, 256, "%s%s", BASE_DIR, "input/");
  } else {
    snprintf(input_dir, 256, "%s%s", BASE_DIR, "output/");
  }

  // set output path
  char output_dir[256] = {'\0'};
  snprintf(output_dir, 256, "%s%s", BASE_DIR, "output/");

  // set glob string based on phase
  char input_globstr[256] = {'\0'};
  if (phase == LEXICON_GENERATION) {
    snprintf(input_globstr, 256, "%s%s", input_dir, "*.wet");
  } else if (phase == LEXICON_SORTING) {
    snprintf(input_globstr, 256, "%s%s", input_dir, "*.lexicon");
  } else if (phase == IINDEX_GENERATION) {
    snprintf(input_globstr, 256, "%s%s", input_dir, "*.lexicon");
  } else if (phase == IINDEX_MERGING) {
    snprintf(input_globstr, 256, "%s%s", input_dir, "*.lexicon");
  } else {
    // bugged, never going here
    abort();
  }

  glob_t results;
  glob(input_globstr, 0, NULL, &results);
  if (results.gl_pathc == 0) {
    return NULL;
  }

  int times = 0;
  if (phase == LEXICON_GENERATION) {
    times = 2;
  } else if (phase == LEXICON_SORTING) {
    times = 1;
  } else if (phase == IINDEX_GENERATION) {
    times = 4;
  } else if (phase == IINDEX_MERGING) {
    times = 3;
  }

  char **pp_flist = (char **)malloc(sizeof(char *) * results.gl_pathc*times+1);
  char **pp_flist_saved = pp_flist;

  char output_file[256] = {'\0'};
  mkdir(output_dir, 0755);

  int i = 0;
  for (i = 0; i < results.gl_pathc; i++) {

    // for input filename
    *pp_flist = (char *)malloc(strlen(results.gl_pathv[i])+1);
    memset(*pp_flist, 0, strlen(results.gl_pathv[i])+1);
    strncpy(*pp_flist, results.gl_pathv[i], strlen(results.gl_pathv[i]));
    pp_flist++;

    // for output filename in pair
    if (phase == LEXICON_GENERATION) {
      snprintf(output_file, 256, "%s%s%s", output_dir, results.gl_pathv[i] + strlen(input_dir), ".lexicon");
      *pp_flist = (char *)malloc(strlen(output_file)+1);
      memset(*pp_flist, 0, strlen(output_file)+1);
      strncpy(*pp_flist, output_file, strlen(output_file));
      pp_flist++;
    } else if (phase == IINDEX_GENERATION) {
      snprintf(output_file, 256, "%s%s%s", output_dir, results.gl_pathv[i] + strlen(input_dir), ".git");
      *pp_flist = (char *)malloc(strlen(output_file)+1);
      memset(*pp_flist, 0, strlen(output_file)+1);
      strncpy(*pp_flist, output_file, strlen(output_file));
      pp_flist++;

      snprintf(output_file, 256, "%s%s%s", output_dir, results.gl_pathv[i] + strlen(input_dir), ".mit");
      *pp_flist = (char *)malloc(strlen(output_file)+1);
      memset(*pp_flist, 0, strlen(output_file)+1);
      strncpy(*pp_flist, output_file, strlen(output_file));
      pp_flist++;

      snprintf(output_file, 256, "%s%s%s", output_dir, results.gl_pathv[i] + strlen(input_dir), ".iidx");
      *pp_flist = (char *)malloc(strlen(output_file)+1);
      memset(*pp_flist, 0, strlen(output_file)+1);
      strncpy(*pp_flist, output_file, strlen(output_file));
      pp_flist++;
    } else if (phase == IINDEX_MERGING) {
      snprintf(output_file, 256, "%s%s%s", output_dir, results.gl_pathv[i] + strlen(input_dir), ".git");
      *pp_flist = (char *)malloc(strlen(output_file)+1);
      memset(*pp_flist, 0, strlen(output_file)+1);
      strncpy(*pp_flist, output_file, strlen(output_file));
      pp_flist++;

      snprintf(output_file, 256, "%s%s%s", output_dir, results.gl_pathv[i] + strlen(input_dir), ".mit");
      *pp_flist = (char *)malloc(strlen(output_file)+1);
      memset(*pp_flist, 0, strlen(output_file)+1);
      strncpy(*pp_flist, output_file, strlen(output_file));
      pp_flist++;
    }
  }
  // for the last filename pointer, put NULL for terminator
  *pp_flist = NULL;

  globfree(&results);

  return pp_flist_saved;
}

/*
 * open two FILE * pointers for word id generation
 */
void open_word_idx_fps(FILE *fp_idx, FILE *fp_word)
{
  char word_idx_filename[256] = {'\0'};
  snprintf(word_idx_filename, 256, "%s%s", BASE_DIR, "input/");

  return;
}

/*
 *
 */
void open_url_idx_fps(FILE *fp_idx, FILE *fp_url)
{
  return;
}


/*
 * free file list memory buffers
 */
void free_inout_filelist(char **pfiles)
{
  if (pfiles == NULL) {
    return;
  }

  char **p_saved = pfiles;

  while (*pfiles != NULL) {
    free(*pfiles);
    pfiles++;
  }

  free(p_saved);
}

