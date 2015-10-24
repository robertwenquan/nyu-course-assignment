#ifndef _page_rank_h
#define _page_rank_h

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "utils.h"
#include "iindex_search.h"

typedef struct docs{
  int docid;
  struct docs * next;
} DOCS;

int nextGEQ(MIT_T ** l_docs, int k);
DOCS * get_union(MIT_T *** list_word_mit);
DOCS * get_intersection(MIT_T *** list_word_mit);
void cal_BM25(DOC_LIST * doc_list, int place, MIT_T *** list_word_mit, int * count);
DOC_LIST * ranking_docs(MIT_T *** list_word_mit);
double cal_idf_q(int N, MIT_T** l_mit);
MIT_T * find_mit_entry(MIT_T ** list_word_mit, int docid);
void refill_offsets(DOC_LIST * cur_doc, int place, MIT_T *** list_word_mit, int size);
void sort_docs_list(DOC_LIST * doc_list);

#endif
