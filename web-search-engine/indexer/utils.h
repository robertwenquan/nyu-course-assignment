#ifndef _iigen_utils_h
#define _iigen_utils_h

#include <stdio.h>
#include <time.h>
#include <stdarg.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <assert.h>
#include <sys/stat.h>
#include "warc.h"


// For logging
// credit from https://github.com/drfeelngood/logger/
#define LOG_DEBUG 0
#define LOG_INFO  1
#define LOG_WARN  2
#define LOG_ERROR 3

#define LOG_LEVEL_CHARS "DIWEF"
#define LOG_MAX_MSG_LEN 1024

typedef struct _logger {
  int level;
  char *datetime_format;
  FILE *fp;
} LOGGER_T;

LOGGER_T * logger_create( void );
void logger_free(LOGGER_T *l);
void log_add(LOGGER_T *l, int level, const char *msg);
void log_debug(LOGGER_T *l, const char *fmt, ...);
void log_info(LOGGER_T *l, const char *fmt, ...);
void log_warn(LOGGER_T *l, const char *fmt, ...);
void log_error(LOGGER_T *l, const char *fmt, ...);
// For logging

// For docid
typedef struct __attribute__((__packed__)) {
  unsigned int docid;
  unsigned short url_fileid;
  unsigned int url_offset;
  unsigned short url_length;
  unsigned short doc_fileid;
  unsigned int doc_offset;
  unsigned int doc_length;
  unsigned short content_offset;
  unsigned int content_length;
} URL_IDX_T;

unsigned int get_doc_id(WARC_REC_T *p_warc);
// For docid

// For wordid
typedef struct _wordid_hashtree_node_ {
  char chr;
  unsigned int wordid;
  struct _wordid_hashtree_node_ *next[62];
} WORDID_HASHTREE_NODE_T;

typedef struct __attribute__((__packed__)) {
  unsigned int word_id;
  unsigned int offset;
  unsigned short length:8;
} WORD_IDX_T;

unsigned int get_word_id(char *word);
// For wordid

// For file list
typedef enum {
               LEXICON_GENERATION = 1,
               LEXICON_SORTING,
               IINDEX_GENERATION,
               IINDEX_MERGING
              } PHASE_T;

char ** get_inout_filelist(PHASE_T phase);
void free_inout_filelist(char **pfiles);
// For file list

// Global Index Table
typedef struct __attribute__((__packed__)) {
  unsigned int word_id;
  unsigned int offset;
  unsigned short n_docs;
} GIT_T;

// Middle Index Table
typedef struct __attribute__((__packed__)) {
  unsigned int docid;
  unsigned int offset;
  unsigned short n_places;
} MIT_T;

// Inverted Index Table
typedef struct __attribute__((__packed__)) {
  unsigned int offset;
} IIDX_T;

char * get_basedir();
void docid_range_writeback(char *filename, unsigned int start, unsigned int end);

extern char BASE_DIR[256];

#endif

