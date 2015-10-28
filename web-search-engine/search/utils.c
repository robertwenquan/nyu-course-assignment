/*
 utility functions for the inverted index generator

  - gzip helper functions
  - logging functions
   * credit from https://github.com/drfeelngood/logger/

 */

#include <stdio.h>
#include <glob.h>
//#include <yaml.h>
#include <pthread.h>
#include "utils.h"
#include "word_search.h"


int verbose = 0;
char BASE_DIR[256] = "test_data/tiny30/";
int ndocs_per_lexicon_bucket = 10;
int stats_ndocs = 0;
int stats_avg_doc_lens = 0;

static void load_index_stats();
static void init_wet_filename_mapping();


/*
 * load yaml file and return parser
 */
/*
static yaml_parser_t * load_yaml(FILE *fh)
{
  yaml_parser_t * p_parser = (yaml_parser_t *)malloc(sizeof(yaml_parser_t));

  // Initialize parser //
  if(!yaml_parser_initialize(p_parser))
    fputs("Failed to initialize parser!\n", stderr);

  // Set input file //
  yaml_parser_set_input_file(p_parser, fh);

  return p_parser;
}

static void destroy_yaml(yaml_parser_t *p_parser)
{
  yaml_parser_delete(p_parser);
}
*/

/*
 * load configuration for this searcher
 * config file is stored under
 * search.yml
 */
void load_config()
{
  char config_filename[256] = {'\0'};
  bzero(config_filename, 256);

  snprintf(config_filename, 256, "search.yml");
  if (verbose) {
    printf("loading config file: %s\n", config_filename);
  }

  FILE *fh = fopen(config_filename, "r");
  fclose(fh);

  load_index_stats();
  init_wet_filename_mapping();
  load_word_idx_table();
}

/*
 * get total number of docs for this index
 * sizeof(url_table.idx)/sizeof(URL_IDX_T)
 */
unsigned int get_ndocs()
{
  char filename_fd_url_idx[256] = {'\0'};
  bzero(filename_fd_url_idx, 256);
  snprintf(filename_fd_url_idx, 256, "%s/output/url_table.idx", get_basedir());
  int fd_url_idx = open(filename_fd_url_idx, O_RDONLY);
  assert(fd_url_idx != -1);

  struct stat st1;
  fstat(fd_url_idx, &st1);

  close(fd_url_idx);

  unsigned ndocs = st1.st_size/sizeof(URL_IDX_T);
  return ndocs;
}

/*
 * load index statistics from the stats file
 * the stats file is stored under
 * ${base_dir}/output/index.stats
 * in yaml format
 */
static void load_index_stats()
{
  char stats_filename[256] = {'\0'};
  bzero(stats_filename, 256);

  snprintf(stats_filename, 256, "%s/output/index.stats", get_basedir());
  if (verbose) {
    printf("loading index stats file: %s\n", stats_filename);
  }

  stats_ndocs = get_ndocs();
  stats_avg_doc_lens = 2000;
}

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
    printf(" %-8s: %9d\n", "offset_start", head->offset_start);
    printf(" %-8s: %9d\n", "offset_end", head->offset_end);
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
  printf(" %-12s: %s\n", "url", "fake url");
  printf(" %-12s: %9d\n", "url offset", p_doc_meta->url_offset);
  printf(" %-12s: %9d\n", "url length", p_doc_meta->url_length);
  printf(" %-12s: %9d\n", "doc length", p_doc_meta->doc_length);
  printf(" %-12s: %9d\n", "ctt offset", p_doc_meta->content_offset);
  printf(" %-12s: %9d\n", "ctt length", p_doc_meta->content_length);
  printf("==========================\n");
}

int total_num_docs(){
  return stats_ndocs;
}

void get_git_filename(char *filename)
{
  char git_globstr[256] = {'\0'};
  bzero(git_globstr, 256);
  snprintf(git_globstr, 256, "%s/output/*.git", get_basedir());
  if (verbose) {
    printf("globstr: %s\n", git_globstr);
  }

  glob_t results;
  glob(git_globstr, 0, NULL, &results);
  assert(results.gl_pathc == 1);

  bzero(filename, 256);
  snprintf(filename, 256, "%s", results.gl_pathv[0]);
}

void get_mit_filename(char *filename)
{
  char mit_globstr[256] = {'\0'};
  bzero(mit_globstr, 256);
  snprintf(mit_globstr, 256, "%s/output/*.mit", get_basedir());
  if (verbose) {
    printf("globstr: %s\n", mit_globstr);
  }

  glob_t results;
  glob(mit_globstr, 0, NULL, &results);
  assert(results.gl_pathc == 1);

  bzero(filename, 256);
  snprintf(filename, 256, "%s", results.gl_pathv[0]);
}

void get_iidx_filename_from_docid(int docid, char *filename)
{
  int fileid = docid/ndocs_per_lexicon_bucket;

  char iidx_globstr[256] = {'\0'};
  bzero(iidx_globstr, 256);
  snprintf(iidx_globstr, 256, "%s/output/lex%05d*.iidx", get_basedir(), fileid);
  if (verbose) {
    printf("globstr: %s\n", iidx_globstr);
  }

  glob_t results;
  glob(iidx_globstr, 0, NULL, &results);
  assert(results.gl_pathc == 1);

  bzero(filename, 256);
  snprintf(filename, 256, "%s", results.gl_pathv[0]);
}

int get_avg_doc_length()
{
  return stats_avg_doc_lens;
}

typedef struct wet_file_mapping_t {
  unsigned int min_docid;
  unsigned int max_docid;
  char wet_filename[256];
} WET_MAPPING_T;

WET_MAPPING_T *p_wet_mapping = NULL;

static void init_wet_filename_mapping()
{
  if (verbose) {
    printf("init wet file mapping\n");
  }

  char docid_range_map_filename[256];
  bzero(docid_range_map_filename, 256);

  snprintf(docid_range_map_filename, 256, "%s/output/wet.mapping", get_basedir());

  FILE *fp_docid_range = fopen(docid_range_map_filename, "r");

  ssize_t nread;
  size_t len = 0;
  char * line = NULL;
  int nrec = 0;
  while ((nread = getline(&line, &len, fp_docid_range)) != -1) {
    nrec++;
  }
  if (verbose) {
    printf("%d wet file entries.\n", nrec);
  }

  assert(p_wet_mapping == NULL);
  p_wet_mapping = (WET_MAPPING_T *)malloc(sizeof(WET_MAPPING_T) * nrec);
  assert(p_wet_mapping != NULL);
  WET_MAPPING_T * p_work = p_wet_mapping;

  fseek(fp_docid_range, 0, SEEK_SET);
  while ((nread = getline(&line, &len, fp_docid_range)) != -1) {
    if (verbose) {
      printf("line: %s", line);
    }

    bzero(p_work, sizeof(WET_MAPPING_T));
    char *p_filename = strtok(line, ",");
    snprintf(p_work->wet_filename, 256, "%s/%s", get_basedir(), p_filename);
    char *p_start = strtok(NULL, ",");
    p_work->min_docid = atoi(p_start);
    char *p_end = strtok(NULL, ",");
    p_work->max_docid = atoi(p_end);
    if (verbose) {
      printf("filename: %s [%d-%d]\n", p_work->wet_filename, p_work->min_docid, p_work->max_docid);
    }

    p_work++; 
  }

  fclose(fp_docid_range);
}

void get_wet_filename_from_docid(int docid, char *filename)
{
  assert(p_wet_mapping != NULL);

  WET_MAPPING_T *p_work = p_wet_mapping;

  while (p_work->min_docid != 0 || p_work->max_docid != 0) {
    if (docid >= p_work->min_docid && docid <= p_work->max_docid) {
      bzero(filename, 256);
      strncpy(filename, p_work->wet_filename, 256);
      if (verbose) {
        printf("wet file: %s\n", filename);
      }
      return;
    }
    p_work++;
  }

  // next come here.
  abort();
}

