#ifndef _iigen_utils_h
#define _iigen_utils_h

#include <stdio.h>
#include <time.h>
#include <stdarg.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

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

#endif

