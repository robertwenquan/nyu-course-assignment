#include "iindex_search.h"
#include <fcntl.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <sys/types.h>


/*
 * standard comparison function of GIT entry
 * for bsearch()
 */
int compare_git(const void *rec_a, const void *rec_b)
{
  GIT_T *p_git_a = (GIT_T *)rec_a;
  GIT_T *p_git_b = (GIT_T *)rec_b;

  if (p_git_a->word_id > p_git_b->word_id) {
    return 1;
  }
  else if (p_git_a->word_id == p_git_b->word_id) {
    return 0;
  }
  else {
    return -1;
  }
}

/* compare_mit is literally the same as compare_git
 * as GIT_T and MIT_T has the same structure in terms of comparison
 */
#define compare_mit compare_git

/*
 * query GIT entry based on the word_id
 * input: word id
 * output: an GIT_T entry in the GIT index table
 */
GIT_T * query_git(int word_id)
{
  // Open *.git file and find word_id using binary search
  //char **p = get_inout_filelist(IINDEX_MERGING);
  int fd_git = -1;
  GIT_T *p_return_git = NULL;

  char filename[256] = {'\0'};
  bzero(filename, 256);
  get_git_filename(filename);

  fd_git = open(filename, O_RDONLY);
  if (fd_git == -1) {
    return NULL;
  }

  struct stat st;
  fstat(fd_git, &st);

  void *git_table = mmap(NULL, st.st_size, PROT_READ, MAP_PRIVATE, fd_git, 0);
  if (git_table == MAP_FAILED) {
    close(fd_git);
    return NULL;
  }
  
  printf("mapped git_table at %p\n", git_table);
   
  GIT_T git_search_key = { .word_id = word_id,
                           .offset = 0,
                           .n_docs = 0
                         };
  
  GIT_T * p_git_hit = bsearch((void *)&git_search_key, git_table, \
                              st.st_size/sizeof(GIT_T), sizeof(GIT_T), compare_git);
  if (p_git_hit == NULL) {
    p_return_git = NULL;
    goto _QUERY_GIT_FAILURE;
  }

  printf("found the git entry at %p\n", p_git_hit);

  p_return_git = (GIT_T *)malloc(sizeof(GIT_T));
  if (p_return_git != NULL) {
    memcpy(p_return_git, p_git_hit, sizeof(GIT_T));
  }

_QUERY_GIT_FAILURE:
  munmap(git_table, st.st_size);
  close(fd_git);
  return p_return_git;
}


/*
 * query MIT entry based on the offset and length
 * input: GIT_T entry
 * output: MIT_T entry
 */
MIT_T ** query_mit(GIT_T *p_git)
{
  // Open *.mit file, return a list of MIT_T entries
  if (p_git == NULL) {
    return NULL;
  }

  FILE *fd_mit = NULL;
  MIT_T **p_return_mit = NULL;

  char filename[256] = {'\0'};
  bzero(filename, 256);
  get_mit_filename(filename);

  fd_mit = fopen(filename, "rb");
  if (fd_mit == NULL) {
    printf("Open file failed\n");
    return NULL;
  }

  p_return_mit = (MIT_T **)calloc(p_git->n_docs + 1, sizeof(MIT_T *));

  MIT_T **p_head = p_return_mit;

  if (p_return_mit == NULL) {
    printf("Malloc p_return_mit failed\n");
    fclose(fd_mit);
    return NULL;
  }

  fseek(fd_mit, p_git->offset, SEEK_SET);

  int i = 0;
  for (i = 0; i < p_git->n_docs ; i++) {
    *p_return_mit = (MIT_T *)malloc(sizeof(MIT_T));
    if (p_return_mit == NULL) {
      printf("Malloc p_return_mit failed\n");
      fclose(fd_mit);
      return NULL;
    }
    fread(*p_return_mit, sizeof(MIT_T), 1, fd_mit);
    p_return_mit++;
  }

  fclose(fd_mit);
  return p_head;
}


/*
 * query inverted index based on the offset and length
 * input: MIT_T entry
 * output: inverted index list
 */

IIDX_T * query_compressed_iindex(MIT_T * p_mit)
{
  /*
  char filename[256] = {'\0'};
  bzero(filename, 256);
  get_iidx_filename_from_docid(p_mit->docid, filename);
    printf("total_num: %d", 000);

  FILE * f_iidx;
  if (p_return_iidx == NULL) {
    return NULL;
  }

  f_iidx = fopen(filename, "r");
  if (f_iidx == NULL) {
    return NULL;
  }

  fseek(f_iidx, p_mit->offset, SEEK_SET);
  fread(p_read ,sizeof(IIDX_T), p_mit->n_places, f_iidx);

  */
  // FOR TEST USE
  p_mit->n_places = 8; 
  IIDX_T * p_read = (IIDX_T *)calloc((p_mit->n_places+1), sizeof(IIDX_T));
  IIDX_T * p_return_iidx = (IIDX_T *)calloc((p_mit->n_places+1), sizeof(IIDX_T));

  p_read[0].offset = 536887297;
  p_read[1].offset = 545259525;
  p_read[2].offset = 1086374277;

  int total_num = p_mit->n_places;
  int i = 0;
  int local_num = 0;
  int i_write = 0;
  int waste = 0;
  int bit = 0;
  int j = 0;

  while (total_num > 0) {
    local_num = p_read[i].offset >> 28;
    printf("total_num: %d\n", total_num);
    printf("local : %d\n", local_num);
    printf("i: %d\n", i);
    bit = 28/local_num;
    waste = 28 - local_num * bit;

    j = 0;

    i_write += local_num;

    while( j < local_num ){
      p_return_iidx[i_write - j - 1].offset = p_read[i].offset % (int)(pow(2,bit));
      p_read[i].offset /= (int)(pow(2,bit));
      j++;
    }

    i++;
    total_num -= local_num;
  }

  int k = 0;
  for(k = 0; k < 8; k++) {
    printf("offsets: %d\n", p_return_iidx[k].offset);
  }

  printf("OUTPUT SHOULD BE:\n 1 \n 1 \n 512 \n 5 \n 6 \n 3 \n 3 \n 5 \n");
  //fclose(f_iidx);
  return p_return_iidx;

}
IIDX_T * query_iindex(MIT_T *p_mit)
{
  char filename[256] = {'\0'};
  bzero(filename, 256);
  get_iidx_filename_from_docid(p_mit->docid, filename);
  int i = 0;

  FILE * f_iidx;
  IIDX_T * p_return_iidx = (IIDX_T *)calloc((p_mit->n_places+1), sizeof(IIDX_T));
  if (p_return_iidx == NULL) {
    return NULL;
  }
  p_return_iidx[p_mit->n_places].offset = -1;
  f_iidx = fopen(filename, "r");

  if (f_iidx == NULL) {
    return NULL;
  }

  fseek(f_iidx, p_mit->offset, SEEK_SET);
  fread(p_return_iidx ,sizeof(IIDX_T), p_mit->n_places, f_iidx);

  fclose(f_iidx);

  for (i = 1; i < p_mit->n_places; i++) {
    p_return_iidx[i].offset += p_return_iidx[i-1].offset;
  }

  return p_return_iidx;
}
