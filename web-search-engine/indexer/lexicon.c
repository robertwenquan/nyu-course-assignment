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
#include <time.h>

static int lexicon_compare(const void *p1, const void *p2);

int docid_saved = 0;
time_t time_saved = 0;


static void get_lex_filename(unsigned long doc_id, int *fileid, char *lex_filename, int buflen)
{
  char * base_dir = get_basedir();
  static char path[] = "output";
  static char name[] = "lex";

  static int bucket_size = 50000;
  *fileid = doc_id / bucket_size;

  bzero(lex_filename, 256);
  snprintf(lex_filename, 256, "%s/%s/%s%05d.%s", base_dir, path, name, *fileid, "lexicon");
}


/*
 * write back one lexicon to file
 */
static void write_back_lexicon(LEXICON_T lex)
{
  static int lex_file_id_inuse = -1;
  static FILE *fp_lex_file = NULL;
  static char lex_file_name[256] = {'\0'};

  int lex_file_id = -1;
  get_lex_filename(lex.docid, &lex_file_id, lex_file_name, 256);

  if (lex_file_id != lex_file_id_inuse) {
    if (fp_lex_file != NULL) {
      fclose(fp_lex_file);
    }

    printf("create lex filename %s starting docid[%d]\n", lex_file_name, lex.docid);
    fp_lex_file = fopen(lex_file_name, "wb");
    assert(fp_lex_file != NULL);

    lex_file_id_inuse = lex_file_id;
  }

  /*
  static char buffer[8*1024*1024] = {'\0'};
  static unsigned int offset = 0;

  if (offset + sizeof(LEXICON_T) >= 8*1024*1024) {
    int ret = fwrite(buffer, offset, 1, fpo);
    assert(ret == 1);
    offset = 0;
  }

  memcpy(buffer + offset, &lex, sizeof(LEXICON_T));
  offset += sizeof(LEXICON_T);
  */
  fwrite(&lex, sizeof(LEXICON_T), 1, fp_lex_file);
}

/*
 * tokenize words from the page content
 * with filtering strategy
 * and generate lexicons
 */
static void tokenize_page_content(char *buffer, int size, unsigned int docid)
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
      write_back_lexicon(lex);
    }

    TKDestroy(tokenizer);
}

static void process_lexicons_from_file(char *infile)
{
  FILE * fp = warc_open(infile);
  int docid_rec_flag = -1;
  unsigned int docid_start = 0;
  unsigned int docid_end = 0;
  unsigned int docid = 0;

  printf("processing %s ...\n", infile);

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
    docid = get_doc_id(p_warc);

    if (docid_rec_flag == -1) {
      docid_start = docid;
      docid_rec_flag = 1;
    }

    int dps = 0;
    time_t ts;
    time(&ts);
    if (ts - time_saved > 3) {
      dps = (docid - docid_saved)/3;
      if (docid_saved != 0) {
        struct tm * tm = localtime(&ts);
        char timestr[32] = {'\0'};
        snprintf(timestr, 32, "%d-%02d-%02d %02d:%02d:%02d", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec);
        printf("%s Processed %d docs, %d docs per sec.\n", timestr, docid, dps);
      }
      time_saved = ts;
      docid_saved = docid;
    }

    // tokenize lexicons from page
    tokenize_page_content(page_content, page_lens, docid);

    // dispose the WARC entry after consumption
    destroy_warc_rec(p_warc);
  }
  warc_close(fp);

  docid_end = docid;

  printf("%s doc id range(%u->%u)\n", infile, docid_start, docid_end);
  docid_range_writeback(infile, docid_start, docid_end);

  return;
}

void * thr_process_lexicons_from_file(void *argv)
{
  char **p = (char **)argv;

  char infile[256] = {'\0'};

  strncpy(infile, *p, 256);

  process_lexicons_from_file(infile);

  return NULL;
}

int lexicon_generator()
{
  char **p = get_inout_filelist(LEXICON_GENERATION);
  char **p_save = p;

  if (p == NULL) {
    return 1;
  }

  time_t ts;
  time(&ts);
  struct tm * tm = localtime(&ts);
  char timestr[32] = {'\0'};
  snprintf(timestr, 32, "%d-%02d-%02d %02d:%02d:%02d", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec);

  printf("%s Building lexicons...\n", timestr);

  int nthreads = 1;
  pthread_t thr[nthreads];
  int thr_idx = 0;
  int loopi = 0;

  while (*p != NULL && *(p+1) != NULL) {

    memset(&thr[thr_idx], 0, sizeof(pthread_t));
    pthread_create(&thr[thr_idx], NULL, thr_process_lexicons_from_file, p);
    usleep(100000);
    thr_idx++;

    if (thr_idx == nthreads) {
      for (loopi=0;loopi<thr_idx;loopi++) {
        pthread_join(thr[loopi], NULL);
      }
      thr_idx = 0;
    }

    p += 2;
  }

  for (loopi=0;loopi<thr_idx;loopi++) {
    pthread_join(thr[loopi], NULL);
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

/*
 * sort one lexicon file in place
 */
static void sort_one_lexicon(char *filename)
{
  int fd = open(filename, O_RDWR);
  assert(fd > 0);

  struct stat st;
  fstat(fd, &st);

  void *src = mmap (0, st.st_size, PROT_READ|PROT_WRITE, MAP_SHARED, fd, 0);
  assert(src != NULL);
  qsort(src, st.st_size / sizeof(LEXICON_T), sizeof(LEXICON_T), lexicon_compare);
  close(fd);
}

/*
 * sorting all lexicons
 */
int lexicon_sorter()
{
  char **p = get_inout_filelist(LEXICON_SORTING);
  char **p_save = p;

  if (p == NULL) {
    return 1;
  }

  time_t ts;
  time(&ts);
  struct tm * tm = localtime(&ts);
  char timestr[32] = {'\0'};
  snprintf(timestr, 32, "%d-%02d-%02d %02d:%02d:%02d", tm->tm_year+1900, tm->tm_mon+1, tm->tm_mday, tm->tm_hour, tm->tm_min, tm->tm_sec);

  printf("%s Sorting lexicons...\n", timestr);

  while (*p != NULL) {
    sort_one_lexicon(*p);
    p++;
  }

  free_inout_filelist(p_save);
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

