#include <stdio.h>
#include <stdlib.h>
#include "utils.h"
#include "../search/utils.h"

void compress_iidx();
void compress_docid();
void simple_9_compress(IIDX_T * IIDX_old, IIDX_T * IIDX_new, int n_places, int * delta_offset);
void fresh_iidx(IIDX_T * IIDX_buf, int num, int start, IIDX_T * IIDX_new, int new_places);
void compress_mit();
void sort_mit();
