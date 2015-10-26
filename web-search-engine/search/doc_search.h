#ifndef _search_url_h
#define _search_url_h

#include <stdio.h>
#include <stdlib.h>
#include "utils.h"

URL_IDX_T * get_doc_meta(unsigned int docid);
int get_doc_length(int docid);
char * get_doc_url(unsigned int docid);

#endif

