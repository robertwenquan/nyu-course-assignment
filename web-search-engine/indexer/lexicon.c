#include "lexicon.h"
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

char** get_lexicon_files()
{
  // hard-coded input data
  char **pp_flist = (char **)malloc(sizeof(char *) * 4);

  char *lexicon_files[] = {"test_data/input/input1.warc.wet", \
                           "test_data/input/input2.warc.wet", \
                           "test_data/input/input3.warc.wet", \
                           NULL \
                          };

  memcpy(pp_flist, lexicon_files, sizeof(char *) * 4);
  return pp_flist;
}

void process_lexicons_from_file(char *filename)
{
  /*
  if is_compressed_with_gzip(filename)
  {
    data
  }

  data = read_data(filename);
   */

  FILE * fp = warc_open(filename);
  printf("file: %s, fp: %p\n", filename, fp);
  while (1) {
    WARC_REC_T *p_warc = warc_get_next(fp);
    if (p_warc == NULL) {
      break;
    }
    printf("offset: %d\n", p_warc->offset);
  }

  return;
}

int lexicon_generator()
{
  char **p = get_lexicon_files();
  char **p_save = p;

  while (*p != NULL)
  {
    process_lexicons_from_file(*p);
    p++;
  }

  free(p_save);
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
  char *filename2 = "test_data/phase2_output/input1.warc.lexicon.2";
  /*
  char *filename1 = "/data/wse/100k/phase1_output/CC-MAIN-20150728002301-00000-ip-10-236-191-2.ec2.internal.warc.lexicon";
  char *filename2 = "/data/wse/100k/bbb.lexicon";
  */

  int fd = open(filename1, O_RDWR);
  struct stat st;
  fstat(fd, &st);

  printf("file: %s, size: %zu, fd = %d\n", filename1, st.st_size, fd);

  int fd_out = open(filename2, O_RDWR | O_CREAT | O_TRUNC, 0755);

  void *src = mmap (0, st.st_size, PROT_READ, MAP_SHARED, fd, 0);
  //printf("src pointer %p, aligned at %lu\n", src, ((unsigned long)(src)%4096));

  //void *dst = mmap (0, st.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd_out, 0);
  //printf("dst pointer %p, aligned at %d\n", dst, ((int)dst%4096));

  void *data = (void *)malloc(st.st_size);
  memcpy(data, src, st.st_size);

  qsort(data, st.st_size / sizeof(LEXICON_T), sizeof(LEXICON_T), lexicon_compare);

  int bytes_write = 0;
  while (bytes_write < st.st_size && bytes_write != -1) { 
    int nbytes = write(fd_out, data, st.st_size);
    printf("write %d in %d\n", nbytes, bytes_write);
    bytes_write += nbytes;
  }

  if (bytes_write == -1) {
    printf("failed to sort lexicons.\n");
  }

  close(fd);
  close(fd_out);

  return 0;
}


#ifdef __TEST__
int main(int argc, char *argv[])
{
  lexicon_generator();
  lexicon_sorter();

  return 0;
}
#endif

