#include "compress.h"

IIDX_T * IIDX_buf;
FILE ** IIDX_files;
long C_offset;

void fake_main();

void compress_iidx()
{
  /*
   * Input : .mit file
   * Output: compressed corresponding iidx file
   *  1. Read each mit entry, update offset
   *  2. Find corresponding iidx file, get all offset numbers
   *  3. Call simple_9 to compress
   *  4. Write back compressed numbers
   *  5. Update global offset
   */

  // Suppose get the list of iidx files and passed by a pointer
  C_offset = 0;

  FILE * f_mit = fopen("test_data/output/input1.warc.wet.lexicon00.mit", "rb+");
  if (f_mit == NULL) {
    return;
  } 
  FILE * f_iidx = fopen("test_data/output/input1.warc.wet.lexicon.iidx", "wb+");
  if (f_iidx == NULL) {
    return;
  } 
  MIT_T * cur_mit = (MIT_T *)calloc(1, sizeof(MIT_T));

  while (!feof(f_mit)) {
    fread(cur_mit, sizeof(MIT_T), 1, f_mit);

    cur_mit->offset = C_offset;
    //fseek(f_mit, -sizeof(MIT_T), SEEK_CUR);
    //fwrite(&cur_mit, sizeof(MIT_T), 1, f_mit);
    //fseek(f_mit, sizeof(MIT_T), SEEK_CUR);
    
    printf("cur_mit: %d\n",cur_mit->n_places);
    IIDX_buf = (IIDX_T *) calloc (cur_mit->n_places + 1, sizeof(IIDX_T));
    simple_9_compress(IIDX_buf, f_iidx);
    free(IIDX_buf);
  } 
  return;
}

void simple_9_compress(IIDX_T * IIDX_buf, FILE * f_iidx)
{
  int n_places = sizeof(IIDX_buf)/sizeof(IIDX_T *) - 1;

  int max_num = 14;

  int count = 1;
  int local_num = 0;
  int cur = 0;

  for(int i = 0; i < n_places; i++){
    cur = IIDX_buf[i].offset;
    if (cur < 4) {
      local_num = 14;
    } else if (cur < 8) {
      local_num = 9;
    } else if (cur < 16) {
      local_num = 7;
    } else if (cur < 32) {
      local_num = 5;
    } else if (cur < 128) {
      local_num = 4;
    } else if (cur < 512) {
      local_num = 3;
    } else if (cur < 19264) {
      local_num = 2;
    } else {
      local_num = 1;
    }

    if (local_num < count) {
      fresh_iidx(IIDX_buf, count - 1, i+1-count, f_iidx);
      i--;
      max_num = 14;
    } 

    if (local_num < max_num) {
      max_num = local_num;
    }

    if (count == max_num) {
      fresh_iidx(IIDX_buf, count, i+1-count, f_iidx);

      max_num = 14;
    }

    count ++;
  }
  return;
}

void fresh_iidx(IIDX_T * IIDX_buf, int num, int start, FILE * f_iidx)
{
  //(int *) buffer = (int *)calloc(1, sizeof(int));

  /* 
   * 1. First 4 bit, store num;
   * 2. According to num, distribute 28 bits to IIDX_buf[start], ..., IIDX_buf[start + num - 1]
   * 3. Write back to f_iidx
   * 4. Update C_offset by 1
   */
  return;
}
void compress_mit()
{
  sort_mit();
  return;
}

void sort_mit()
{
  return;
}

