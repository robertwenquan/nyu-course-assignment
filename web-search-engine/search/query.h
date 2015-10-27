#ifndef _search_query_h
#define _search_query_h

#include <stdio.h>
#include <stdlib.h>
#include "utils.h"
#include "word_search.h"
#include "iindex_search.h"
#include "doc_search.h"
#include "page_search.h"

char **tokenize_input(char *input_line, int *nwords);
void process_query(char ** search_keywords, int nwords, int fd);

#endif
