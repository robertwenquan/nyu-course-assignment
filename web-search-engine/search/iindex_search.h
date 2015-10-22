#ifndef _search_iindex_h
#define _search_iindex_h

#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

GIT_T * query_git(int word_id);
MIT_T ** query_mit(GIT_T *p_git);
IIDX_T * query_iidx(MIT_T *pmit);
char * get_iidx_file(int docid);
#endif

