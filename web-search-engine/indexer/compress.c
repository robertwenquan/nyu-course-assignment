#include "compress.h"

IIDX_T * IIDX_old;
IIDX_T * IIDX_new;
FILE ** IIDX_files;
long C_offset;

void fake_main();

void compress_docid(){
  char filename[256] = {'\0'};
  char filename_new[256] = {'\0'};

  bzero(filename_new, 256);
  snprintf(filename_new, 256, "%s%s%s%s", get_basedir(), "output/", "final", ".mit.new");
  FILE * f_mit_new = fopen(filename_new, "wb");
  if (f_mit_new == NULL) {
    printf("Compress Doc ID failed");
    return;
  }

  bzero(filename, 256);
  snprintf(filename, 256, "%s%s%s%s", get_basedir(), "output/", "final", ".git");
  FILE * f_git = fopen(filename, "rb");
  if (f_git == NULL) {
    printf("Compress Doc ID failed");
    return;
  }

  bzero(filename, 256);
  snprintf(filename, 256, "%s%s%s%s", get_basedir(), "output/", "final", ".mit");
  FILE * f_mit = fopen(filename, "rb");
  if (f_mit == NULL) {
    printf("Compress Doc ID failed");
    return;
  }

  MIT_T * mit_buf = NULL;
  int n_docs = 0;
  GIT_T * git_buf = (GIT_T *)calloc(1, sizeof(GIT_T));
  int i = 0;
  int last = 0;
  while (!feof(f_git)) {
    last = 0;
    fread(git_buf , sizeof(GIT_T), 1, f_git);
    n_docs = git_buf->n_docs;
    mit_buf = (MIT_T *)calloc(n_docs, sizeof(MIT_T));
    fread(mit_buf, sizeof(MIT_T), n_docs, f_mit);

    for (i = 0; i < n_docs; i++) {
      mit_buf[i].docid -= last;
      last += mit_buf[i].docid;
    }

    fwrite(mit_buf, sizeof(MIT_T), n_docs, f_mit_new);
    free(mit_buf);
  }

  free(git_buf);
  fclose(f_mit);
  fclose(f_git);
  fclose(f_mit_new);

  remove(filename);
  rename(filename_new, filename);
  return;
}
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

  FILE * f_mit = fopen("test_data/output/final.mit", "rb");
  if (f_mit == NULL) {
    return;
  } 
  FILE * f_mit_new = fopen("test_data/output/final.mit.new", "wb");
  if (f_mit_new == NULL) {
    return;
  } 
  FILE * f_iidx = fopen("test_data/output/lex00000.lexicon", "rb");
  if (f_iidx == NULL) {
    return;
  } 
  FILE * f_iidx_new = fopen("test_data/output/lex00000.lexicon.new", "wb");
  if (f_iidx_new == NULL) {
    return;
  } 

  MIT_T * cur_mit = (MIT_T *)calloc(1, sizeof(MIT_T));

  int delta_offset = 0;

  while (!feof(f_mit)) {
    fread(cur_mit, sizeof(MIT_T), 1, f_mit);

    IIDX_old = (IIDX_T *) calloc (cur_mit->n_places + 1, sizeof(IIDX_T));
    IIDX_new = (IIDX_T *) calloc (cur_mit->n_places + 1, sizeof(IIDX_T));

    // Find start of offset according to cur_mit->offset
    fseek(f_iidx, cur_mit->offset, SEEK_SET);

    // Read cur_mit->n_places IIDX_T entries
    fread(IIDX_old, sizeof(IIDX_T), cur_mit->n_places, f_iidx);

    // Compress offset
    simple_9_compress(IIDX_old, IIDX_new, cur_mit->n_places, &delta_offset);

    // Write compressed data to new file
    fwrite(IIDX_new, sizeof(IIDX_T), delta_offset, f_iidx_new);

    // Write updated offset of cur_mit->offset
    cur_mit->offset = C_offset;
    fwrite(cur_mit, sizeof(MIT_T), 1, f_mit_new);

    // Update new global offset of iidx_new file
    C_offset += delta_offset * sizeof(IIDX_T);

    free(IIDX_new);
    free(IIDX_old);
  } 
  fclose(f_mit);
  fclose(f_mit_new);
  fclose(f_iidx);
  fclose(f_iidx_new);
  rename("test_data/output/lex00000.lexicon.new", "test_data/output/lex00000.lexicon");
  rename("test_data/output/final.mit.new", "test_data/output/final.mit");
  return;
}

void simple_9_compress(IIDX_T * IIDX_old, IIDX_T * IIDX_new, int n_places, int * delta_offset)
{
  int max_num = 14;

  int count = 1;
  int local_num = 0;
  int cur = 0;
  int new_place = 0;
  int used = 0;
  int i = 0;

  for(i = 0; i < n_places; i++){
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
      used += count-1;
      new_place++;
      i--;
      max_num = 14;
      count = 0;
    } 

    if (local_num < max_num) {
      max_num = local_num;
    }

    if (count == max_num) {
      fresh_iidx(IIDX_old, count, i+1-count, IIDX_new, new_place);
      used += count;
      new_place++;
      max_num = 14;
      count = 0;
    }

    count ++;
  }

  if (used != n_places) {
    fresh_iidx(IIDX_old, count-1, i+1-count, IIDX_new, new_place);
    new_place++;
  }

  *delta_offset = new_place ;
  return;
}

void fresh_iidx(IIDX_T * IIDX_old, int num, int start, IIDX_T * IIDX_new, int new_place)
{
  //(int *) buffer = (int *)calloc(1, sizeof(int));

  /* 
   * 1. First 4 bit, store num;
   * 2. According to num, distribute 28 bits to IIDX_buf[start], ..., IIDX_buf[start + num - 1]
   * 3. Write back to f_iidx
   * 4. Update C_offset by 1
   */
  int bit = 28/num;

  int ret = 0;
  ret += num << 28;
  int i = 0;
  for(i = 0; i < num; i++) {
    ret += IIDX_old[start+i].offset << ((num-i-1)*bit);
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

