#include "compress.h"

IIDX_T * IIDX_old;
IIDX_T * IIDX_new;
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

  FILE * f_mit = fopen("test_data/output/lex00000.lexicon00.mit", "rw");
  if (f_mit == NULL) {
    return;
  } 
  FILE * f_iidx = fopen("test_data/output/input1.warc.wet.lexicon.iidx", "wb+");
  if (f_iidx == NULL) {
    return;
  } 
  MIT_T * cur_mit = (MIT_T *)calloc(1, sizeof(MIT_T));

  int delta_offset = 0;

  while (!feof(f_mit)) {
    fread(cur_mit, sizeof(MIT_T), 1, f_mit);

    IIDX_old = (IIDX_T *) calloc (cur_mit->n_places + 1, sizeof(IIDX_T));
    IIDX_new = (IIDX_T *) calloc (cur_mit->n_places + 1, sizeof(IIDX_T));

    fseek(f_iidx, cur_mit->offset, SEEK_SET);
    fread(IIDX_old, sizeof(IIDX_T), cur_mit->n_places, f_iidx);
    simple_9_compress(IIDX_old, IIDX_new, cur_mit->n_places, &delta_offset);
    fseek(f_iidx, C_offset, SEEK_SET);
    fwrite(IIDX_new, sizeof(IIDX_T), delta_offset, f_iidx);

    cur_mit->offset = C_offset;
    fseek(f_mit, -sizeof(MIT_T), SEEK_CUR);
    fwrite(&cur_mit, sizeof(MIT_T), 1, f_mit);
    fseek(f_mit, sizeof(MIT_T), SEEK_CUR);
    
    C_offset += delta_offset * sizeof(IIDX_T);

    free(IIDX_new);
    free(IIDX_old);

    // TODO: Don't know why it can't stop
    break;
  } 
  fclose(f_mit);
  fclose(f_iidx);
  return;
}

void simple_9_compress(IIDX_T * IIDX_old, IIDX_T * IIDX_new, int n_places, int * delta_offset)
{
  int max_num = 14;

  int count = 1;
  int local_num = 0;
  int cur = 0;
  int new_place = 0;

  for(int i = 0; i < n_places; i++){
    cur = IIDX_old[i].offset;
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
      fresh_iidx(IIDX_old, count - 1, i+1-count, IIDX_new, new_place);
      new_place++;
      i--;
      max_num = 14;
    } 

    if (local_num < max_num) {
      max_num = local_num;
    }

    if (count == max_num) {
      fresh_iidx(IIDX_old, count, i+1-count, IIDX_new, new_place);
      new_place++;
      max_num = 14;
    }

    count ++;
  }

  *delta_offset = new_place + 1 ;
  return;
}

void fresh_iidx(IIDX_T * IIDX_buf, int num, int start, IIDX_T * IIDX_new, int new_place)
{
  //(int *) buffer = (int *)calloc(1, sizeof(int));

  /* 
   * 1. First 4 bit, store num;
   * 2. According to num, distribute 28 bits to IIDX_buf[start], ..., IIDX_buf[start + num - 1]
   * 3. Write back to f_iidx
   * 4. Update C_offset by 1
   */
  int count = 0;
  int bit = 0;
  switch (num) {
    case 14:
    case 13:
    case 12:
    case 11:
    case 10:
      count = 7;
      bit = 2;
      break;
    case 9:
    case 8:
      count = 6;
      bit = 3;
      break;
    case 7:
    case 6:
      count = 5;
      bit = 4;
      break;
    case 5:
      count = 4;
      bit = 5;
      break;
    case 4:
      count = 3;
      bit = 7;
      break;
    case 3:
      count = 2;
      bit = 8;
      break;
    case 2:
      count = 1;
      bit = 14;
      break;
    case 1:
      count = 0;
      bit = 28;
      break;
    default:
      return;
  }

  int ret = 0;
  ret += count << 28;
  int i = 0;
  for(i = 0; i < num; i++) {
    ret += IIDX_new[start+i].offset << ((num-i-1)*bit);
  }

  IIDX_new[new_place].offset = ret;
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

