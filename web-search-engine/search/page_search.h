#ifndef _search_page_h
#define _search_page_h

#include <stdio.h>
#include <stdlib.h>
#include "utils.h"
#include "doc_search.h"

typedef struct _page_struct_t_ {
  int docid;
  int word_id;
  int offset;
  char context[256];
} PAGE_CONTEXT_T;

#endif

