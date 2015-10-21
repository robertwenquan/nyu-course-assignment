#ifndef _iigen_lexicon_h
#define _iigen_lexicon_h

#include <stdio.h>
#include <ctype.h>
#include "warc.h"
#include "utils.h"
#include "tokenizer.h"

int lexicon_generator();

typedef struct __attribute__((__packed__)) {
  unsigned int word_id;
  unsigned int offset;
  unsigned short length:8;
} WORD_IDX_T;

// lexicon structure
// the output format of phase1 and phase2
// the output binary file will be N x sizeof(LEXICON_T)
typedef struct __attribute__((__packed__)) {
  unsigned int word_id;
  unsigned int docid;
  unsigned int offset;
  unsigned short context;
} LEXICON_T;

#endif

