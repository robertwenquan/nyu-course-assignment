#ifndef _page_rank_h
#define _page_rank_h

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "utils.h"

int nextGEQ(MIT_T ** l_docs, int k);
int * get_intersection(MIT_T *** list_word_mit);
double cal_BM25(int docid, MIT_T *** list_word_mit);
char * ranking_docs(int * docs);
int get_doc_length(int docid);
int get_avg_doc_length();
int total_num_docs();
double cal_idf_q(int N, MIT_T** l_mit);
MIT_T * find_doc(MIT_T ** list_word_mit, int docid);
#endif
