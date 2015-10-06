#ifndef _iigen_utils_h
#define _iigen_utils_h

#include <stdio.h>

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

