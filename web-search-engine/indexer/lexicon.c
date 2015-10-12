#include "lexicon.h"
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <glob.h>
#include <pthread.h>
#include <unistd.h>

static int lexicon_compare(const void *p1, const void *p2);


/*
 * write back one lexicon to file
 */
static void write_back_lexicon(LEXICON_T lex, FILE *fpo)
{
  static char buffer[8*1024*1024] = {'\0'};
  static unsigned int offset = 0;

  if (offset + sizeof(LEXICON_T) >= 8*1024*1024) {
    int ret = fwrite(buffer, offset, 1, fpo);
    assert(ret == 1);
    offset = 0;
  }

  memcpy(buffer + offset, &lex, sizeof(LEXICON_T));
  offset += sizeof(LEXICON_T);
}

/*
 * tokenize words from the page content
 * with filtering strategy
 * and generate lexicons
 */
static void tokenize_page_content(char *buffer, int size, unsigned int docid, FILE *fpo)
{
    TokenizerT *tokenizer = NULL;
    tokenizer = TKCreate(" \t\r\n`~!@#$%^&*()_+-=[]{}\\|;':\",.<>/?", buffer, size);

    char *pmatch = buffer;
    char *token = NULL;
    unsigned int offset = 0;
    while ( (token = TKGetNextToken(tokenizer)) ) {

      // skip all non alpha num words
      size_t length = strlen(token);

      int i;
      short skip = 0;
      for (i = 0; i < length; i++) {
        char c = token[i];
        if (!isalnum(c)) {
          skip = 1;
          break;
        }
      }

      if (skip == 1) {
        continue;
      }

      // skip all single character or single digit
      if (length == 1) {
        continue;
      }

      unsigned int wordid = get_word_id(token);
      pmatch = strstr(pmatch, token);
      offset = pmatch - buffer;

      #ifdef __DEBUG__
      assert(strncmp(token, pmatch, strlen(token)) == 0);
      #endif

      LEXICON_T lex = {.word_id=wordid,\
                       .docid=docid,\
                       .offset=offset,\
                       .context=2\
                      };

      //printf(">> wordid: %d, docid: %d, %s, start %p, offset %u\n", lex.word_id, lex.docid, token, buffer, lex.offset);
      write_back_lexicon(lex, fpo);
    }

    TKDestroy(tokenizer);
}

static void process_lexicons_from_file(char *infile, char *outfile)
{
  FILE * fp = warc_open(infile);
  FILE * fpo = fopen(outfile, "wb");

  printf("infile: %s, fp: %p\n", infile, fp);
  printf("outfile: %s, fp: %p\n", outfile, fpo);

  while (1) {

    // get the next WARC entry
    WARC_REC_T *p_warc = warc_get_next(fp);
    if (p_warc == NULL) {
      break;
    }

    // skip the WARC records which is not "conversion" type
    // the first record in WET file is always a meta entry which is not conversion
    // or "text/plain" 
    if (strcmp(p_warc->header->warc_type, "conversion") != 0 || \
        strcmp(p_warc->header->content_type, "text/plain") != 0) {
      continue;
    }

    // tokenize the WARC payload (page content)
    // data is in p_warc->payload->data
    // length is in p_warc->payload->length
    //        or in p_warc->header->content_length
    #ifdef __DEBUG__
    assert(p_warc->payload->length == p_warc->header->content_length);
    #endif

    char *page_content = p_warc->payload->data;
    int page_lens = p_warc->payload->length;
    unsigned int docid = get_doc_id();

    // tokenize lexicons from page
    tokenize_page_content(page_content, page_lens, docid, fpo);

    // dispose the WARC entry after consumption
    destroy_warc_rec(p_warc);
  }
  fclose(fpo);
  warc_close(fp);

  // sort the lexicon in place
  int fd = open(outfile, O_RDWR);
  assert(fd > 0);

  struct stat st;
  fstat(fd, &st);

  void *src = mmap (0, st.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
  assert(src != NULL);
  qsort(src, st.st_size / sizeof(LEXICON_T), sizeof(LEXICON_T), lexicon_compare);
  close(fd);

  return;
}

void * thr_process_lexicons_from_file(void *argv)
{
  char **p = (char **)argv;

  char infile[256] = {'\0'};
  char outfile[256] = {'\0'};

  strncpy(infile, *p, 256);
  strncpy(outfile, *(p+1), 256);

  process_lexicons_from_file(infile, outfile);

  return NULL;
}

int lexicon_generator()
{
  char **p = get_inout_filelist(LEXICON_GENERATION);
  char **p_save = p;

  if (p == NULL) {
    return 1;
  }

  int nthreads = 4;
  pthread_t thr[nthreads];
  int thr_idx = 0;

  while (*p != NULL && *(p+1) != NULL) {

    memset(&thr[thr_idx], 0, sizeof(pthread_t));
    pthread_create(&thr[thr_idx], NULL, thr_process_lexicons_from_file, p);
    usleep(100000);
    thr_idx++;

    if (thr_idx == nthreads) {
      int i=0;
      for (i=0;i<nthreads;i++) {
        pthread_join(thr[i], NULL);
      }
    }

    p += 2;
  }

  free_inout_filelist(p_save);
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


#ifdef __TEST__
int main(int argc, char *argv[])
{
  lexicon_generator();

  return 0;
}
#endif

