#ifndef _iigen_utils_h
#define _iigen_utils_h

#include <stdio.h>

// lexicon structure
// the output format of phase1 and phase2
// the output binary file will be N x sizeof(LEXICON_T)
typedef struct __attribute__((__packed__)) {
  unsigned int word_id;
  unsigned int docid;
  unsigned int offset;
  unsigned short context;
} LEXICON_T;

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

