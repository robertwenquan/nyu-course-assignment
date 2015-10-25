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

//char BASE_DIR[] = "/data/wse/100k/";
char BASE_DIR[] = "test_data";
int ndocs_per_lexicon_bucket = 1000;

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
unsigned int get_doc_id()
{
  static int docid = 0;
  static pthread_mutex_t docid_lock;

  pthread_mutex_lock(&docid_lock);
  docid++;
  pthread_mutex_unlock(&docid_lock);

  return docid;
}

static WORDID_HASHTREE_NODE_T wordid_hash_root;

/*
 * char to index for word id hash sub-tree query
 */
int char_to_index(char chr)
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

/*
 * print the git entry for debugging
 */
void print_git_entry(GIT_T *p_git) {
  printf("===== GIT Entry =====\n");
  printf(" %-8s: %9d\n", "word id", p_git->word_id);
  printf(" %-8s: %9d\n", "offset", p_git->offset);
  printf(" %-8s: %9d\n", "ndocs", p_git->n_docs);
  printf("=====================\n");
}


/*
 * print the mit entry for debugging
 */
void print_mit_entry(MIT_T *p_mit) {
  printf("===== MIT Entry =====\n");
  printf(" %-8s: %9d\n", "docid", p_mit->docid);
  printf(" %-8s: %9d\n", "offset", p_mit->offset);
  printf(" %-8s: %9d\n", "nplaces", p_mit->n_places);
  printf("=====================\n");
}

void print_iidx_entry(IIDX_T *p_iidx) {
  printf("===== IIDX Entry =====\n");
  printf(" %-8s: %9d\n", "offset", p_iidx->offset);
  printf("=====================\n");
}

void print_doc_list(DOC_LIST * head) {
  while(head != NULL) {
    if (head->docid == -1 ){
      break;
    }
    printf("===== DOC LISTS=====\n");
    printf(" %-8s: %9d\n", "doc_id", head->docid);
    printf(" %-8s: %9f\n", "score", head->score);
    printf(" %-8s: \n", "offsets");
    while(*(head->offsets) != -1) {
      printf(" %-8s: %9d\n", " ", *(head->offsets) );
      (head->offsets)++;
    }
    head++;
  }
}

void print_doc_meta_entry(URL_IDX_T *p_doc_meta)
{
  printf("===== DOC META Entry =====\n");
  printf(" %-12s: %9d\n", "docid", p_doc_meta->docid);
  printf(" %-12s: %9d\n", "url offset", p_doc_meta->url_offset);
  printf(" %-12s: %9d\n", "url length", p_doc_meta->url_length);
  printf(" %-12s: %9d\n", "doc length", p_doc_meta->doc_length);
  printf(" %-12s: %9d\n", "ctt offset", p_doc_meta->content_offset);
  printf(" %-12s: %9d\n", "ctt length", p_doc_meta->content_length);
  printf("==========================\n");
}

int stats_ndocs = 288;
int stats_avg_doc_lens = 2000;

int total_num_docs(){
  return stats_ndocs;
}

void get_git_filename(char *filename)
{
  bzero(filename, 256);
  snprintf(filename, 256, "%s", "test_data/tiny30/output/input1.warc.wet.lexicon00.git");
}

void get_mit_filename(char *filename)
{
  bzero(filename, 256);
  snprintf(filename, 256, "%s", "test_data/tiny30/output/input1.warc.wet.lexicon00.mit");
}

void get_iidx_filename_from_docid(int docid, char *filename)
{
  bzero(filename, 256);

  int fileid = 0;
  fileid = docid/ndocs_per_lexicon_bucket;

  //snprintf(filename, 256, "%s/%s/%s%05d.iidx", BASE_DIR, "output", "xxxx", fileid);
  snprintf(filename, 256, "%s", "test_data/tiny30/output/input2.warc.wet.lexicon.iidx");
}

int get_avg_doc_length()
{
  return stats_avg_doc_lens;
}
