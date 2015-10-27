/**************************************************************************/
/* usage  ./merge maxdegree memsize finlist outfileprefix                 */
/*                                                                        */
/*        maxdegree      : n-way merge                                    */
/*        memsize        : size of available memory in bytes              */
/*        finlist        : name of file containing a list of input files  */
/*        outfileprefex  : directory to record intermediate files         */
/*                                                                        */
/* For example:                                                           */
/*          ./merge 8 4096 finlist fout                                   */
/**************************************************************************/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include "utils.h"
#include "merge.h"


static char ** merge_files(char** p);
static int write_min(int i, int degree);
static int sort_curr(int degree);
static int merge_cont(int degree);
static void check_ith_mit(int i);
static void get_next_word(int i);
static void buf_initiate(unsigned char *buf_space, int degree);

BUF_T *ioBufs;
GIT_T *topElem;
int buf_size;
int max_degree = 8;
int mem_size = 4096000;
int out_offset;


void merge_iindex(char **p) {

  while (*p != NULL && *(p+1) != NULL && *(p+2) != NULL && *(p+3) != NULL) {
    p = merge_files(p);
    if (p == NULL) {
      printf("Merge Failed!\n");
      return;
    }
  }

  char filename[256] = {'\0'};
  bzero(filename,256);

  if (*(p+1) != NULL) {
    snprintf(filename, 256, "%s%s%s%s", get_basedir(), "output/", "final", ".git");
    rename(*(p+1), filename);
  }

  bzero(filename,256);

  if (*(p+2) != NULL) {
    snprintf(filename, 256, "%s%s%s%s", get_basedir(), "output/", "final", ".mit");
    rename(*(p+2), filename);
  }
  compress_docid();
  return;
}

char** merge_files(char **p) {
/* Merge files listed in inputlist, every max_degree files produce a new file
   Then return the output list */ 

  int degree = 0;
  int i = 0;
  int numFile = 0;
  int ret = 0;
  int length = 0;
  char outfile[1024] = {'\0'};
  char outmit[1024] = {'\0'};
  char outgit[1024] = {'\0'};
  char basename[1024] = {'\0'};

  char **plist = (char **)malloc(sizeof(char *) * 200);
  if (plist == NULL) {
    return NULL;
  }
  memset(plist, 0, sizeof(char *) * 200);
  char **phead = plist;
  char **p_in = p;

  unsigned char *buf_space = NULL;
  buf_space = (unsigned char *)malloc(mem_size);
  if (buf_space == NULL) {
    printf("Malloc %d byte failed", mem_size);
    return NULL;
  }
  memset(buf_space, 0, mem_size);

  ioBufs = (BUF_T *)malloc((max_degree + 1) * sizeof(BUF_T));
  if (ioBufs == NULL) {
    printf("Malloc memory for ioBufs failed.\n");
    return NULL;
  }
  memset(ioBufs, 0, (max_degree + 1) * sizeof(BUF_T));

  sprintf(basename, "%s%d", *p, 0);

  while (*p != NULL && *(p+1) != NULL && *(p+2) != NULL) {
    //Initiate for each pile of files.
    out_offset = 0;

    /*Get source files from the list, assign each file to a BUFFER structure,
      at most max_degree files each time.*/
    for (degree = 0; degree < max_degree; degree++) {
      if (*p == NULL || *(p+1) == NULL || *(p+2) == NULL) {
        break;
      }

      ioBufs[degree].fgit = fopen(*(p+1), "r");
      if (ioBufs[degree].fgit == NULL) {
        return NULL;
      }

      ioBufs[degree].fmit = fopen(*(p+2), "r");
      if (ioBufs[degree].fmit == NULL) {
        return NULL;
      }

      p += 3;
    }

    if (degree == 0) {
      break;
    }

    /* Merge several viles into one file,
       Result of each N files stored in file00, file01, file02...
       Prepared for next level merge */ 

    sprintf(outfile, "%s%d", basename, numFile);

    sprintf(outgit, "%s%s", outfile, ".git");
    ioBufs[degree].fgit = fopen(outgit, "w");
    if (ioBufs[degree].fgit == NULL) {
      printf("%s doesn't exist\n", outgit);
      return NULL;
    }

    sprintf(outmit, "%s%s", outfile, ".mit");
    ioBufs[degree].fmit= fopen(outmit, "w");
    if (ioBufs[degree].fmit == NULL) {
      printf("%s doesn't exist\n", outmit);
      return NULL;
    }

    //Initiate BUF_F for each file.
    buf_initiate(buf_space, degree);

    //Merge the current "degree" files
    ret = merge_cont(degree);
    if (ret == -1) {
      return NULL;
    }

    //close files
    for (i = 0; i <= degree; i++) {
      fclose(ioBufs[i].fgit);
      fclose(ioBufs[i].fmit);
    }

    //write the name of output file into outputlist
    length = strlen(basename);
    *plist = (char *)malloc(length+1);
    bzero(*plist, length+1);
    memcpy(*plist, basename, length);
    plist++;

    length = strlen(outgit);
    *plist = (char *)malloc(length+1);
    bzero(*plist, length+1);
    memcpy(*plist, outgit, length);
    plist++;

    length = strlen(outmit);
    *plist = (char *)malloc(length+1);
    bzero(*plist, length+1);
    memcpy(*plist, outmit, length);
    plist++;

    numFile++;
  }

  free(ioBufs);
  free(buf_space);

  while ( *p_in != NULL && *(p_in+1) != NULL && *(p_in+2) != NULL ){
    remove(*(p_in+1));
    remove(*(p_in+2));
    p_in += 3;
  }
  return phead;
}

static void buf_initiate(unsigned char *buf_space, int degree) {
  /* Initiate start of each file buffer.
     Divide buf_space to 3*degree part.
     Give output file more buffer.         */

  buf_size = mem_size / ( degree * 3 * sizeof(GIT_T) );

  int i = 0;
  for (i = 0; i <= degree; i++) {
    ioBufs[i].bufgit = (GIT_T *) &(buf_space[ i * sizeof(GIT_T)*buf_size * 2]);
    ioBufs[i].bufmit = (MIT_T *) &(buf_space[ i * sizeof(GIT_T)*buf_size * 2 + sizeof(GIT_T)* buf_size ]);
    ioBufs[i].gitTotal = 0;
    ioBufs[i].gitConsume = 0;
    ioBufs[i].mitTotal = 0;
    ioBufs[i].mitConsume = 0;
  }

  ioBufs[degree].bufmit= (MIT_T *) &(buf_space[ degree * sizeof(GIT_T)* buf_size * 2 + sizeof(GIT_T)* buf_size * degree/ 2 ]);
  ioBufs[degree].gitTotal =  buf_size * degree/ 2 ;
  ioBufs[degree].mitTotal = degree * buf_size - buf_size * degree/ 2 ;

  return;
}

static void get_next_word(int i) {
/* Load next git record of ith file to topElem struct
   Prepared for next comparition. */
  if (i == -1) {
    return;
  }

  BUF_T *b = &(ioBufs[i]);
  int j,k;
  // If all record in buffer has been used, reload from file.
  if ( b->gitTotal == b->gitConsume) {
    for (j = 0; j < buf_size / 2; j++) {
      k = fread(&b->bufgit[j], sizeof(GIT_T), 1, b->fgit);
      if (k == 0) {
        break;
      }
    }
    b->gitTotal = j;
    b->gitConsume = 0;  
  }

  // No more record in the file, set topElem[i].word_id to -1.
  if (b->gitTotal == 0) {
    topElem[i].word_id = -1;
    return;
  }

  // Copy the current BUF_F in buffer to topElem[i].
  memcpy(&topElem[i], &(b->bufgit[b->gitConsume]), sizeof(GIT_T));
  b->gitConsume += 1;

  return;
}

static int merge_cont(int degree) {
  /* Get the minimum of the top element of each buffer
     Write it into ioBufs[degree], which is the buffer of output file
     Refill with the next element of this buffer block
     Until all the buffer block is empty. */
  int ret = 0;

  topElem = (GIT_T *)malloc(sizeof(GIT_T) * (degree + 1));
  if (topElem == NULL) {
    printf("Malloc memory for topElem failed.\n");
    return -1;
  }
  memset(topElem, 0, sizeof(GIT_T) * (degree + 1));

  // Initiate topElem[i] with the first record of each input file.
  int i;
  for (i = 0; i < degree ; i++) {
    get_next_word(i);
  }
 
  int min = 0;

  // If all files are done, min = -1.
  while (min >= 0) {
    // Get the order of buffer with minimum word_id
    min = sort_curr(degree);
    // Copy minimum to output buffer
    ret = write_min(min, degree);
    if (ret != 0) {
      return -1;
    }
    // Update record of that buffer
    get_next_word(min);
  } 

  free(topElem);
  return 0;
}

static int sort_curr(int degree) {
  /* Get the minimum word_id and return it's order in buffer */

  int minPos = -1;

  int i = 0;
  for (i = 0; i < degree; i++) {
    if (topElem[i].word_id != -1) {
      if (minPos == -1) {
        minPos = i;
      } else if (topElem[i].word_id < topElem[minPos].word_id) {
        minPos = i;
      }
    }
  }

  return minPos;
}

static int write_min(int i, int degree) {
  /* The ith buffer block contains the current minimum word_id, write it's information to output file. */

  BUF_T *b = &ioBufs[i];
  BUF_T *out = &ioBufs[degree];
  int ret = 0;

  // If i == -1, means every buffer is empty, write back everything.
  if (i == -1) {
    // Write the last record in topElem[degree] to BUF_F buffer
    if (out->gitTotal == out->gitConsume) {
      int j;
      for (j = 0; j < out->gitConsume; j++) {
        ret = fwrite(&(out->bufgit[j]), sizeof(GIT_T), 1, out->fgit);
        if (ret == 0) {
          printf("Write file failed");
          return -1;
        }
      }
      out->gitTotal = buf_size * degree/ 2;
      out->gitConsume = 0;
    }

    memcpy(&(out->bufgit[out->gitConsume]), &topElem[degree], sizeof(GIT_T));
    out->gitConsume += 1;

    // Flush everything to disk
    int j;
    for (j = 0; j < out->gitConsume; j++) {
      ret = fwrite(&(out->bufgit[j]), sizeof(GIT_T), 1, out->fgit);
      if (ret == 0) {
        printf("Write file failed");
        return -1;
      }
    }

    for (j = 0; j < out->mitConsume; j++) {
      ret = fwrite(&(out->bufmit[j]), sizeof(MIT_T), 1, out->fmit);
      if (ret == 0) {
        printf("Write file failed");
        return -1;
      }
    }

    return 0;
  }

  //get the size of docs of that word, write to output buffer one by one.
  int size = topElem[i].n_docs;
  while (size > 0) {
    out_offset += 1;

    // Refill content of ith buffer
    if (b->mitTotal == b->mitConsume) {
      check_ith_mit(i);
    }

    // If there is no enough space to write a record, flush to disk
    if (out->mitTotal == out->mitConsume ) {
      int j;
      for (j = 0; j < out->mitConsume; j++) {
        ret = fwrite(&(out->bufmit[j]), sizeof(MIT_T), 1, out->fmit);
        if (ret == 0) {
          printf("Write file failed");
          return -1;
        }
      }

      out->mitTotal = degree * buf_size - buf_size * degree/ 2 ;
      out->mitConsume = 0;
    }

    // Copy MIT record to output buffer.
    memcpy(&out->bufmit[out->mitConsume], &b->bufmit[b->mitConsume], sizeof(MIT_T));
    b->mitConsume += 1; 
    out->mitConsume += 1;
    size--;
  }

  /* If topElem[i].word_id is different with topElem[degree]
    then write topElem[degree] to output file 
    and update topElem[degree]                              */
  if (topElem[i].word_id != topElem[degree].word_id ) {

    if (out->gitTotal == out->gitConsume) {
      int j;
      for (j = 0; j < out->gitConsume; j++) {
        ret = fwrite(&(out->bufgit[j]), sizeof(GIT_T), 1, out->fgit);
        if (ret == 0) {
          printf("Write file failed");
          return -1;
        }
      }

      out->gitTotal = buf_size * degree/ 2;
      out->gitConsume = 0;
    }

    if (topElem[i].n_docs != out_offset) {
      memcpy(&(out->bufgit[out->gitConsume]), &topElem[degree], sizeof(GIT_T));
      out->gitConsume += 1;
    }

    memcpy(&topElem[degree], &topElem[i], sizeof(GIT_T));
    topElem[degree].offset = (out_offset - topElem[i].n_docs) * sizeof(GIT_T);
  }else {
    // If they are the same, update topElem[degree].n_docs
    topElem[degree].n_docs += topElem[i].n_docs;
  }

  return 0;
}

static void check_ith_mit(int i) {
  /* Refill buffer of ioBufs[i] when all of them are used */

  BUF_T *b = &ioBufs[i];
  
  int j, k;
  for (j = 0; j < buf_size ; j++) {
    k = fread(&b->bufmit[j], sizeof(MIT_T), 1, b->fmit);
    if (k == 0) {
      break;
    }
  }

  b->mitTotal = j;
  b->mitConsume = 0;

  return;
}

