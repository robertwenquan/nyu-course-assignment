#include "lexicon.h"
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

int lexicon_generator()
{
  return 0;
}

/*
 * lexicon comparison function, used for qsort()
 *
 * compare key1: word_id
 * compare key2: docid
 * compare key3: offset
 *
 */
static int lexicon_compare(const void *p1, const void *p2)
{
  LEXICON_T *lex1 = (LEXICON_T *)p1;
  LEXICON_T *lex2 = (LEXICON_T *)p2;

  unsigned int word_id1 = lex1->word_id;
  unsigned int word_id2 = lex2->word_id;

  unsigned int doc_id1 = lex1->docid;
  unsigned int doc_id2 = lex2->docid;

  unsigned int off1 = lex1->offset;
  unsigned int off2 = lex2->offset;

  // compare word_id
  if (word_id1 > word_id2) {
    return 1;
  }
  else if (word_id1 < word_id2) {
    return -1;
  }

  // if word_id equals, compare docid
  if (doc_id1 > doc_id2) {
    return 1;
  }
  else if (doc_id1 < doc_id2) {
    return -1;
  }

  // when word_id and docid both equals
  // compare offset
  if (off1 > off2) {
    return 1;
  }
  else if (off1 < off2) {
    return -1;
  }

  return 0;
}

/*
 * sort lexicon based on word_id, docid, and offset
 *
 * after sorting, the lexicons will be placed in word_id order
 * for the lexicons with the same word_id, they will be placed
 * in docid order, and then offset order
 *
 */
int lexicon_sorter()
{
  char *filename1 = "test_data/phase1_output/input1.warc.lexicon";
  char *filename2 = "test_data/bbb/input1.warc.lexicon";

  int fd = open(filename1, O_RDWR);
  struct stat st;
  fstat(fd, &st);

  printf("file: %s, size: %llu, fd = %d\n", filename1, st.st_size, fd);

  int fd_out = open(filename2, O_RDWR | O_CREAT | O_TRUNC, 0755);
  printf("fd2 = %d\n", fd_out);

  void *src = mmap (0, st.st_size, PROT_READ, MAP_SHARED, fd, 0);
  printf("src pointer %p, aligned at %d\n", src, ((int)src%4096));

  //void *dst = mmap (0, st.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd_out, 0);
  //printf("dst pointer %p, aligned at %d\n", dst, ((int)dst%4096));

  void *data = (void *)malloc(st.st_size);
  memcpy(data, src, st.st_size);

  qsort(data, st.st_size / sizeof(LEXICON_T), sizeof(LEXICON_T), lexicon_compare);

  write(fd_out, data, st.st_size);

  close(fd);
  close(fd_out);

  return 0;
}


#ifdef __TEST__
int main(int argc, char *argv[])
{
  lexicon_sorter();
  lexicon_generator();
}
#endif

