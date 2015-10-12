#include "lexicon.h"
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <glob.h>
#include <sys/stat.h>

char BASE_DIR[] = "/data/wse/1m/";

static int lexicon_compare(const void *p1, const void *p2);


/*
 * get input file list to work on for lexicon generation
 *
 * input will be in ${BASE_DIR}/input/ *.wet
 * output will be in ${BASE_DIR}/output/ *.lexicon
 *
 * return value:
 *  an array of char * with full path filenames
 *    two filenames are in a group
 *    [input1, output1, input2, output2, input3, output3, ...]
 */
static char ** get_lexicon_files()
{
  char input_dir[256] = {'\0'};
  snprintf(input_dir, 256, "%s%s", BASE_DIR, "input/");
  char output_dir[256] = {'\0'};
  snprintf(output_dir, 256, "%s%s", BASE_DIR, "output/");

  char input_globstr[256] = {'\0'};
  snprintf(input_globstr, 256, "%s%s", input_dir, "*.wet");

  glob_t results;
  glob(input_globstr, 0, NULL, &results);
  if (results.gl_pathc == 0) {
    return NULL;
  }

  char **pp_flist = (char **)malloc(sizeof(char *) * results.gl_pathc*2+1);
  char **pp_flist_saved = pp_flist;

  char output_file[256] = {'\0'};
  mkdir(output_dir, 0755);

  int i = 0;
  for (i = 0; i < results.gl_pathc; i++) {

    // for input filename
    *pp_flist = (char *)malloc(strlen(results.gl_pathv[i])+1);
    memset(*pp_flist, 0, strlen(results.gl_pathv[i])+1);
    strncpy(*pp_flist, results.gl_pathv[i], strlen(results.gl_pathv[i]));
    pp_flist++;

    // for output filename in pair
    snprintf(output_file, 256, "%s%s%s", output_dir, results.gl_pathv[i] + strlen(input_dir), ".lexicon");
    *pp_flist = (char *)malloc(strlen(output_file)+1);
    memset(*pp_flist, 0, strlen(output_file)+1);
    strncpy(*pp_flist, output_file, strlen(output_file));
    pp_flist++;
  }
  // for the last filename pointer, put NULL for terminator
  *pp_flist = NULL;

  globfree(&results);

  return pp_flist_saved;
}

/*
 * free file list memory buffers
 */
static void free_lexicon_files(char **pfiles)
{
  if (pfiles == NULL) {
    return;
  }

  char **p_saved = pfiles;

  while (*pfiles != NULL) {
    free(*pfiles);
    pfiles++;
  }

  free(p_saved);
}

/*
 * write back one lexicon to file
 */
static void write_back_lexicon(LEXICON_T lex, FILE *fpo)
{
  fwrite(&lex, sizeof(LEXICON_T), 1, fpo);
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
  fflush(fpo);
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

int lexicon_generator()
{
  char **p = get_lexicon_files();
  char **p_save = p;

  if (p == NULL) {
    return 1;
  }

  while (*p != NULL && *(p+1) != NULL) {
    process_lexicons_from_file(*p, *(p+1));
    p += 2;
  }

  free_lexicon_files(p_save);
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
static int lexicon_sorter()
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

  #ifdef __MACOS__
  printf("file: %s, size: %lld, fd = %d\n", filename1, st.st_size, fd);
  #endif
  #ifdef __LINUX__
  printf("file: %s, size: %zu, fd = %d\n", filename1, st.st_size, fd);
  #endif

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

  return 0;
}
#endif

