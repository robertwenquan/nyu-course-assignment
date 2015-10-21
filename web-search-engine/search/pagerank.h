#ifndef _page_rank_h
#define _page_rank_h

#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

int nextGEQ(MIT_T ** l_docs, int k);
int * get_intersection(MIT_T *** list_word_mit);
float cal_BM25 (int doc_id);
char * ranking_docs(int * docs);
#endif
